%define pfx /opt/freescale/rootfs/%{_target_cpu} 

%define cs_version 4.3-74

Summary         : A GNU collection of binary utilities.
Name            : binutils
Version         : 2.18
Release         : 3
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : Development/Tools
Source          : %{name}-%{version}.tar.bz2
Patch0          : %{name}-%{cs_version}-from-fsf-2_18.diff.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This binutils package is built using binutils-2.18 plus the binutils patch
from the CodeSourcery %{cs_version} release:
binutils-%{cs_version}-from-fsf-2_18.diff

The binutils tarball can be obtained from any of the GNU ftp sites or their
mirrors.
The CodeSourcery patch can be obtained by downloading the source rpm:
freescale-powerpc-linux-gnu-%{cs_version}.src.rpm from:
http://www.codesourcery.com/gnu_toolchains/power/download.html and then
extracting the binutils patch from this source rpm.


%Prep
%setup
%patch0 -p1


%Build

# Temporary hack - stevep
# For building toolchain components an optimized version of the
# target is needed.  This should really be defined in the config
# area of ltib, and not done in the toolchain spec files.
# For now we assume that the optimised target can be derived by
# stripping the trailing "-" off the toolchain prefix, but this
# will not be true for all cases, eg when using uClibc toolchains.
if [ ${TOOLCHAIN_PREFIX} = "arm_v6_vfp_le-" -o -n "$UCLIBC" ]
then
	OPT_CFGHOST=$CFGHOST
else
	OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`
fi

# Ensure that build is never the same as host or target.
BINUTILS_BUILD=`echo %{_build} | sed s/-/-build_/`

rm -rf build-binutils
mkdir build-binutils
cd build-binutils
export CPP=$BUILDCPP
CC_FOR_BUILD="${BUILDCC}" \
../configure \
    --host=${OPT_CFGHOST} --build=${BINUTILS_BUILD} --target=${OPT_CFGHOST} \
    --prefix=%{_prefix} --disable-nls --enable-multilib=no --mandir=%{_mandir}


# Hack to prevent documentation from getting built.
if [ -z "${PKG_BINUTILS_BUILD_DOCS}" ]
then
perl -pi.bak -e 'if(m,^do-info\:$, || m,^do-dvi\:$, || m,^do-pdf\:$, || m,^do-html\:$, || m,^do-install-info\:$, || m,^do-install-pdf\:$, || m,^do-install-html\:$,) { $do_edit = 1; next }; if(m,^\.PHONY\:\s+info-host$, || m,^\.PHONY\:\s+dvi-host$, || m,^\.PHONY\:\s+pdf-host$, || m,^\.PHONY\:\s+html-host$, || m,^\.PHONY\:\s+install-info-host$, || m,^\.PHONY\:\s+install-pdf-host$, || m,^\.PHONY\:\s+install-html-host$,) { $do_edit = 0 }; if($do_edit) { print "#" }' Makefile
fi

make CC_FOR_BUILD="${BUILDCC}" all

%Install

# Hack to prevent any multilib directories from getting installed since we are
# building for a single library target root file system.  Setting
# --enable-multilib=no to configure doesn't appear to have any effect, so
# hence this hack!  :-( 
# If this hack isn't used the result is package build failures with multilib
# toolchains when binutils is built due to the addition of the multilib
# directory component to the linker search path which doesn't exist on the
# target root file system.  Stevep
perl -pi.orig -e 's,^MULTIOSDIR\s+=\s+.*-print-multi-os-directory.*,MULTIOSDIR = \.,;' build-binutils/libiberty/Makefile

cd build-binutils
make CC_FOR_BUILD="${BUILDCC}" DESTDIR=${RPM_BUILD_ROOT}/%{pfx} install

# Remove libtool .la files.
find $RPM_BUILD_ROOT/%{pfx} -name \*.la -exec rm {} \;


%Clean
rm -rf ${RPM_BUILD_ROOT}


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define pkg_name uClibc
%define linux_libc_headers   linux-libc-headers-2.6.12.0
%define linux_kernel_headers linux-2.6.20

Summary         : uClibc - a Small C Library for Linux
Name            : uclibc
Version         : r18301
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes/Steve Papacharalambous
Group           : System Environment/Libraries
Source          : %{pkg_name}-%{version}.tar.bz2
Source1         : %{linux_libc_headers}.tar.bz2
Source2         : %{linux_kernel_headers}.tar.bz2
Patch0          : uclibc-getopt_h-groff.patch
Patch1          : uclibc-rcmd_c-inetutils.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

See: http://www.uclibc.org/

%Prep

%setup -n %{pkg_name}
%patch0 -p1
%patch1 -p1


%Build

if [ ! -e linux/include/asm ] 
then
    if grep -q 'CONFIG_PPC_MERGE=y' $PLATFORM_PATH/$PKG_KERNEL_PRECONFIG
    then
        LINTARCH=powerpc
    fi
    if [ "$LINTARCH" = "ppc" ]
    then
        tar jxvf %{SOURCE1}
        mv %{linux_libc_headers} linux
        ln -s asm-$LINTARCH linux/include/asm
    else
        tar jxvf %{SOURCE2}
        cd %{linux_kernel_headers}
        cp $PLATFORM_PATH/$PKG_KERNEL_PRECONFIG .config || exit 1

        yes "" | make ARCH=${LINTARCH} HOSTCC="$BUILDCC" oldconfig
        make ARCH=${LINTARCH} HOSTCC="$BUILDCC" INSTALL_HDR_PATH=$RPM_BUILD_DIR/%{pkg_name}/linux headers_install
        cd - 
    fi
fi
test -L include/asm         || \
 ln -fs $RPM_BUILD_DIR/%{pkg_name}/linux/include/asm include/asm
test -L include/asm-generic || \
 ln -fs $RPM_BUILD_DIR/%{pkg_name}/linux/include/asm-generic include/asm-generic
test -L include/linux       || \
 ln -fs $RPM_BUILD_DIR/%{pkg_name}/linux/include/linux include/linux

PKG_UCLIBC_PRECONFIG=${PKG_UCLIBC_PRECONFIG:-uclibc.config}
if [ -f "$PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG" ]
then
    cp $PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG .config
else
    echo "Your platform has no uclibc.config in $PLATFORM_PATH, menuconfig forced"
    PKG_LIBC_WANT_CF=1
fi

# force to use our kernel headers
cat <<TXT >> .config
KERNEL_HEADERS="\$(CURDIR)/include"
UCLIBC_SUSV3_LEGACY_MACROS=y
UCLIBC_SUSV3_LEGACY=y
UCLIBC_HAS_GNU_GLOB=y
PTHREADS_DEBUG_SUPPORT=y
TXT
# fix up namespace compatibility changes
perl -pi -e '
     s,^(# )*HAS_FPU,\1UCLIBC_HAS_FPU,;
     s,ARCH_HAS_NO_MMU=y,# ARCH_HAS_MMU is not set,;
     ' .config
if [ -n "$PKG_LIBC_WANT_CF" -o -n "$SCB_WANT_CF" ]
then
    make menuconfig HOSTCC="$BUILDCC"
    cp .config $PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG
else
    yes "" | make CROSS=${TOOLCHAIN_PREFIX} HOSTCC="$BUILDCC" oldconfig
fi
make CROSS=${TOOLCHAIN_PREFIX} HOSTCC="$BUILDCC"


%Install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT/%{pfx} install

# Install sanitized kernel headers.
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/src
cp -a $RPM_BUILD_DIR/%{pkg_name}/linux $RPM_BUILD_ROOT/%{pfx}/usr/src

# Fix up library paths in libc.so
if [ -f $RPM_BUILD_ROOT/%{pfx}/usr/lib/libc.so ]
then
    cd $RPM_BUILD_ROOT/%{pfx}/usr/lib
    perl -i.orig -p -e 's,/lib/libc.so.0,../../lib/libc.so.0,; s,/usr/lib/uclibc_nonshared.a,./uclibc_nonshared.a,' libc.so
    cd -
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

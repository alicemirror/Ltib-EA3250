%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A collection of basic system utilities
Name            : util-linux
Version         : 2.12
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : util-linux-2.12.tar.gz
Patch0          : util-linux-2.12a-kernel_headers-1.patch
Patch1          : util-linux-2.12-fdiskbsdlabel_h_m68k.patch
Patch2          : util-linux-2.12-cf-bitops_h.patch
Patch3          : util-linux-2.12-fdisk_alignment.patch
Patch4          : util-linux-2.12-iomem-fix.patch

Patch5          : util-linux-2.12-gcc4-lvalue.patch
Patch6          : util-linux-2.12-umount2-gcc4.patch
Patch7          : util-linux-2.12-tqueue-gcc4.patch
Patch8          : util-linux-2.12-uclibc-sys_siglist.patch
Patch9          : util-linux-2.12-syscall-macro-v02.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This is extracted from revision 1.14 in CVS which should be used for
older (2.4) kernels via the pkg_map mechanism.

%Prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
if [ $TOOLCHAIN_PREFIX = "arm_v6_vfp_le-" ]
then
%patch4 -p1
fi
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%Build
# The first part (INSTALLSUID) is only needed during testing until either
# we build using fakeroot or root
perl -pi -e 's,^INSTALLSUID.*,INSTALLSUID=\$(INSTALL) -m \$(SUIDMODE),g;
             s,^LOCALE_DIR=.*,LOCALE_DIR=%{_prefix}/share/locale,;
             s,^CPU=.*,CPU=$ENV{GNUTARCH},;
             s,^ARCH=.*,ARCH=$ENV{GNUTARCH},
            ' MCONFIG

perl -pi -e 's,echo\s+>\s+swapargs\.h,echo "#define SWAPON_HAS_TWO_ARGS" > swapargs.h,' mount/swap.configure

./configure --prefix=%{_prefix}

perl -pi -e 's,^CURSESFLAGS=-I[\w/]+\s+,CURSESFLAGS=,;' make_include

make HAVE_SLN=yes

%Install
rm -rf $RPM_BUILD_ROOT
# the USE_TTY_GROUP can be remove after testing
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx} USE_TTY_GROUP="no"

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



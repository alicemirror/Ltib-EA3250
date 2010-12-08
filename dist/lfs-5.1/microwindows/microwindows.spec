%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Nano-X window display program and samples
Name            : microwindows
Version         : 0.91
Release         : 0
License         : MPL/GPL
Vendor          : Freescale
Packager        : Matt Waddel / Yu Liu
Group           : Applications/System
Source          : microwindows-full-0.91.tar.gz
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
Microwindows (also known as nano-x) is a very small frame buffer
based X server. Its aim is to bring the features of modern windowing
environments to smaller devices and platforms. Also included are
several utility and demo programs.

Package can be got here:
ftp://microwindows.censoft.com/pub/microwindows/microwindows-full-0.91.tar.gz

%Prep
%setup
cd src
case "$LINTARCH" in
    arm*)
        ;;
    i386|i686)
        ;;
    m68k)
        ;;
    ppc|powerpc|ppc64)
	cp -v Configs/config.ppc config
	sed -i '/^ARCH[ \t]*=/a\BIGENDIAN                = Y' config
	eval sed -i \'s@^POWERPCTOOLSPREFIX.*@POWERPCTOOLSPREFIX       = $TOOLCHAIN_PREFIX@\' config
	#sed -i 's@POWERPCTOOLSPREFIX.*$$@POWERPCTOOLSPREFIX       = $TOOLCHAIN_PREFIX@' config
	sed -i 's@^HAVE_SHAREDMEM_SUPPORT.*$@HAVE_SHAREDMEM_SUPPORT   = Y@' config
	sed -i 's@^VTSWITCH.*$@VTSWITCH                 = Y@' config
	sed -i 's@^SERMOUSE.*$@SERMOUSE                 = Y@' config
	sed -i 's@^TPMOUSE.*$@TPMOUSE                  = N@' config
	sed -i '/TTYKBD/a\SCANKBD                  = Y' config
	sed -i '/TTYKBD/d' config
	sed -i 's@-msoft-float@@' Arch.rules
        ;;
    *)
	echo "dont know how to handle mutexes for $LINTARCH"
	exit 1
	;;
esac

sed -i '/^#include <asm\/page.h>.*/d' nanox/clientfb.c
sed -i 's@PAGE_SIZE@getpagesize()@' nanox/clientfb.c
sed -i 's@!(DOS_TURBOC | DOS_QUICKC | _MINIX | VXWORKS)@!(DOS_TURBOC | DOS_QUICKC | _MINIX | VXWORKS | LINUX | UNIX)@' mwin/winevent.c
sed -i '/^extern win \*windows.*/d' demos/nanowm/nanowm.h

%Build
cd src
make -j1 HOSTCC="$BUILDCC"

%Install
INSTALL_DIR="$RPM_BUILD_ROOT/%{pfx}/usr/share/nanox"

rm -rf $RPM_BUILD_ROOT
mkdir -vp $INSTALL_DIR/bin
cd src
cp -a bin/* $INSTALL_DIR/bin
cp -a *.sh $INSTALL_DIR
cp -a include/ $INSTALL_DIR
cp -a lib/ $INSTALL_DIR

BIN_DIR="$RPM_BUILD_ROOT"/%{pfx}/usr/bin
mkdir $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp -a bin/nano-X $BIN_DIR
cp -a bin/nanowm $BIN_DIR
cp -a bin/nxterm $BIN_DIR
cp -a bin/nxclock $BIN_DIR
cp -a bin/nxkbd $BIN_DIR

## Remove these build machine executables. Are they only need during build?
for i in convbmp makebmp convbdf
do
	rm -f $INSTALL_DIR/bin/$i
done
rm -f $INSTALL_DIR/bin/*.gdb

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


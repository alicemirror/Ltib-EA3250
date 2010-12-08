%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : zaptel drivers and utilities
Name            : zaptel
Version         : 1.4.11
Release         : 1
License         : GPL
Vendor          : Digium
Packager        : Vadim Lebedev at mbdsys dot com
Group           : Applications/Communication
Source          : %{name}-%{version}.tar.gz
Source1         : zaptel_rpm_devices.tmpl
Patch1          : zaptel-1.4.11-cross.patch
Patch2          : zaptel-1.4.11-hrt-arch.patch
Patch3          : zaptel-1.4.11-makefw.patch
Patch4          : zaptel-1.4.11-printmodes.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}

PKG_ZAPTEL_PRECONFIG=${PKG_ZAPTEL_PRECONFIG:-zaptel.menuselect.makeopts}
if [ -f "$PLATFORM_PATH/${PKG_ZAPTEL_PRECONFIG}" ]
then
    cp $PLATFORM_PATH/$PKG_ZAPTEL_PRECONFIG menuselect.makeopts
else
    if [ -f "$CONFIG_DIR/defaults/$PKG_ZAPTEL_PRECONFIG" ]
    then
        cp "$CONFIG_DIR/defaults/$PKG_ZAPTEL_PRECONFIG"  menuselect.makeopts
    fi
fi
if [ -n "$PKG_ZAPTEL_WANT_CF" -o -n "$SCB_WANT_CF" ]
then
    make menuconfig HOSTCC='/usr/bin/gcc' HOSTCFLAGS='-B/usr/bin' HOSTLDFLAGS="-B/usr/bin" HOSTLD=/usr/bin/ld HOSTAR=/usr/bin/ar 
    cp menuselect.makeopts $PLATFORM_PATH/$PKG_ZAPTEL_PRECONFIG
fi

KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}
if grep -q 'CONFIG_PPC_MERGE=y' $KBOUT/.config
then
    LINTARCH=powerpc
fi
if [ ! -f $KBOUT/.config ]
then
    cat <<TXT
You need a built unpacked kernel source tree in:
$KBOUT
to build kernel modules
TXT
    exit 1
fi

KVER=`strings $DEV_IMAGE/boot/vmlinux | perl -n -e 'print($1), exit(0) if m,Linux version ([\S]+),'`

make  HOSTCC='/usr/bin/gcc' HOSTCFLAGS='-B/usr/bin' HOSTLDFLAGS="-B/usr/bin" HOSTLD=/usr/bin/ld HOSTAR=/usr/bin/ar KSRC=$KSRC_DIR KVERS=$KVER ARCH=$LINTARCH


%Install
rm -rf $RPM_BUILD_ROOT
KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}
if grep -q 'CONFIG_PPC_MERGE=y' $KBOUT/.config
then
    LINTARCH=powerpc
fi
if [ ! -f $KBOUT/.config ]
then
    cat <<TXT
You need a built unpacked kernel source tree in:
$KBOUT
to build kernel modules
TXT
    exit 1
fi

KVER=`strings $DEV_IMAGE/boot/vmlinux | perl -n -e 'print($1), exit(0) if m,Linux version ([\S]+),'`

make install-modules install-programs ARCH=$LINTARCH DESTDIR=$RPM_BUILD_ROOT/%{pfx} HOSTCC='/usr/bin/gcc' HOSTCFLAGS='-B/usr/bin' HOSTLDFLAGS="-B/usr/bin" HOSTLD=/usr/bin/ld HOSTAR=/usr/bin/ar KSRC=$KSRC_DIR KVERS=$KVER ARCH=$LINTARCH
#sudo make devices ARCH=$LINTARCH DESTDIR=$RPM_BUILD_ROOT/%{pfx} HOSTCC='/usr/bin/gcc' HOSTCFLAGS='-B/usr/bin' HOSTLDFLAGS="-B/usr/bin" HOSTLD=/usr/bin/ld HOSTAR=/usr/bin/ar KSRC=$KSRC_DIR KVERS=$KVER ARCH=$LINTARCH


# create the rpm style device nodes
perl -p -e 's,/pfx,/%{pfx},g' %{SOURCE1} > /tmp/rpm_devices


%Clean
rm -rf $RPM_BUILD_ROOT
rm -f /tmp/rpm_devices

%Files -f /tmp/rpm_devices
%defattr(-,root,root)
%{pfx}/*

%changelog
* Wed Jul 16 2008 Vadim Lebedev <vadim@mbdsys.com>
- Initial version

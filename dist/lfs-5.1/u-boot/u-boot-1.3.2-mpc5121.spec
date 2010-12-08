%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.3.2
Release         : 20080311
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/System
Source          : u-boot-%{version}.tar.bz2
Patch1		: u-boot-1.3.2-ADS5121-001-fsl-diu-move-pixel-clock-setting.patch
Patch2		: u-boot-1.3.2-ADS5121-002-fsl-diu-replace-DPRINTF.patch
Patch3		: u-boot-1.3.2-ADS5121-003-fsl-diu-DIU-support-for-5121ADS.patch
Patch4		: u-boot-1.3.2-ADS5121-004-Support-for-ADS512101-rev-3.patch
Patch5		: u-boot-1.3.2-ADS5121-005-Add-CW-debug-support.patch
Patch6		: u-boot-1.3.2-ADS5121-006-enable-clocks-for-both-uarts.patch			
Patch7		: u-boot-1.3.2-ADS5121-007-jffs2boot-default-boot.patch
Patch8		: u-boot-1.3.2-ADS5121-008-Reduce-FEC-PHY-init-wait.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Open source u-boot v1.3.2

%Prep
%setup -n u-boot-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%Build
if [ -z "$PKG_U_BOOT_CONFIG_TYPE" ]; then
    echo PKG_U_BOOT_CONFIG_TYPE is not set
    exit 1
fi
make distclean
make HOSTCC="$BUILDCC" CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_CONFIG_TYPE
make HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP" \
    CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_BUILD_ARGS

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
for i in u-boot.bin u-boot
do
    cp $i $RPM_BUILD_ROOT/%{pfx}/boot
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

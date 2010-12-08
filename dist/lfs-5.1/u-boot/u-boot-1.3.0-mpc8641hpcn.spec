%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.3.0
Release         : 20080118
License         : GPL
Vendor          : Freescale
Packager        : Ebony Zhu
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch1          : u-boot-fsl-1.3.0-MPC86xx_DCACHE.patch
Patch2          : u-boot-fsl-1.3.0-ATI_FB_X300.patch
Patch3          : u-boot-fsl-1.3.0-USBKB_CTRL.patch
Patch4          : u-boot-fsl-1.3.0-USBKB_STDIN.patch
Patch5          : u-boot-fsl-1.3.0-RIO.patch
Patch6          : u-boot-fsl-1.3.0-MPC8641_RIO_INIT.patch
Patch7          : u-boot-fsl-1.3.0-MPC8641_ASMP-2.patch
Patch8          : u-boot-fsl-1.3.0-MPC86xx_CW.patch
Patch9          : u-boot-fsl-1.3.0-EEPROM.patch
Patch10         : u-boot-fsl-1.3.0-MPC8641_DEFCONF.patch
Patch11         : u-boot-fsl-1.3.0-USB_STOP.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

From Freescale ubootcpdref project plus Freescale patches

%Prep
%setup -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%Build
PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-MPC8641HPCN_config}
make HOSTCC="$BUILDCC" CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_CONFIG_TYPE
make HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP" \
     CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_BUILD_ARGS all


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

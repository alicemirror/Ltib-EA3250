%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.3.0
Release         : 2007
License         : GPL
Vendor          : Freescale
Packager        : Ebony Zhu
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch1          : u-boot-fsl-1.3.0-MPC8548_eTSEC34.patch
Patch2          : u-boot-fsl-1.1.3-MPC85xxCDS_IPADDR-2.patch
Patch3          : u-boot-fsl-1.3.0-MPC8548_BOARD_X31.patch
Patch4          : u-boot-fsl-1.3.0-MPC8548_fix_caslat.patch
Patch5          : u-boot-fsl-1.3.0-MPC8548_freq.patch
Patch6          : u-boot-fsl-1.1.3-MPC85xxCDS_tftp.patch
Patch7          : u-boot-fsl-1.3.0-MPC8548_CPU2.patch
Patch8          : u-boot-fsl-1.2.0-FSL_PCIe_reset.patch
Patch9          : u-boot-fsl-1.3.0-MPC8548_DDR19.patch
Patch10         : u-boot-fsl-1.3.0-RIO.patch
Patch11         : u-boot-fsl-1.3.0-RIO_errata39.patch
Patch12         : u-boot-fsl-1.3.0-MPC8548_RIO_init.patch
Patch13         : u-boot-fsl-1.3.0-MPC8548_eTSEC_Errata86.patch
Patch14         : u-boot-fsl-1.3.0-MPC85xx_CW.patch
Patch15         : u-boot-fsl-1.3.0-MPC85xx_EEPROM-2.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
U-Boot 1.3.0 plus Freescale patches.

%{summary}

All source and patches from Freescale.

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
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%Build
PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-MPC8548CDS_config}
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

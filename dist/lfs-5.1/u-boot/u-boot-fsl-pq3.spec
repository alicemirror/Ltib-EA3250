%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.1.3
Release         : cvs20050607
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : u-boot-cvs-20050607.tar.bz2
Patch0          : u-boot-fsl-1.1.3-MPC8548CDS_PCI.patch
Patch1          : u-boot-fsl-1.1.3-MPC8548CDS_PEX-2.patch
Patch2          : u-boot-fsl-1.1.3-MPC8555CDS_DDR-2.patch
Patch3          : u-boot-fsl-1.1.3-MPC85xxCDS_X31.patch
Patch4          : u-boot-fsl-1.1.3-MPC85xxCDS_IPADDR-2.patch
Patch5          : u-boot-fsl-1.1.3-MPC8548CDS_LAWS.patch
Patch6          : u-boot-fsl-1.1.3-MPC8548CDS_CPU_VERSION.patch
Patch7          : u-boot-fsl-1.1.3-MPC8560ADS_FCC-2.patch
Patch8          : u-boot-fsl-1.1.3-MPC8560ADS_SCC2.patch
Patch9          : u-boot-fsl-1.1.3-MPC8560ADS_debug_port.patch
Patch10         : u-boot-fsl-1.1.3-MPC8540EVAL-2.patch
Patch11         : u-boot-fsl-1.1.3-PQ3_CW.patch
Patch12         : u-boot-fsl-1.1.3-MPC8540EVAL_CodeTEST.patch
Patch13         : u-boot-fsl-1.1.3-MPC85xxCDS_phy.patch
Patch14         : u-boot-fsl-1.1.3-MPC85xxCDS_freq-4.patch
Patch15         : u-boot-fsl-1.1.3-MPC85xxCDS_loadaddr.patch
Patch16         : u-boot-fsl-1.1.3-MPC85xxCDS_id_eeprom2.patch
Patch17         : u-boot-fsl-1.1.3-MPC85xxCDS_tftp.patch
Patch18         : u-boot-fsl-1.1.3-MPC85xxCDS_etsec34-2.patch
Patch19         : u-boot-fsl-1.1.3-MPC85xxCDS_disable_2t.patch
Patch20         : u-boot-fsl-1.1.3-MPC85xxCDS_fix_CPU2.patch
Patch21         : u-boot-fsl-1.1.3-MPC85xxCDS_fix_caslat.patch
Patch22         : u-boot-pq3-gcc4.patch
Patch23         : u-boot-fsl-1.1.3-MPC85xx_gcc4_serial.patch
Patch24         : u-boot-fsl-pq3-Fix-make-3.81.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n u-boot-cvs-20050607
%patch0 -p1
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
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

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

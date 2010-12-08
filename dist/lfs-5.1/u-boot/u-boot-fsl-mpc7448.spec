%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.1.3
Release         : cvs20050725
License         : GPL
Vendor          : Freescale
Packager        : Jason Jin /Roy Zang
Group           : Applications/System
Source          : u-boot-1.1.3.tar.bz2
Patch0          : %{name}-fsl-%{version}-MPC7448_general.patch
Patch1          : %{name}-fsl-%{version}-MPC7448_board.patch
Patch2          : %{name}-fsl-%{version}-MPC7448_config-2.patch
Patch3          : %{name}-fsl-%{version}-MPC7448_tundra-3.patch
Patch4          : %{name}-fsl-%{version}-MPC7448_sata_common-3.patch
Patch5          : %{name}-fsl-%{version}-MPC7448_sata-3.patch
Patch6          : %{name}-fsl-%{version}-MPC7448_cw.patch
Patch7          : u-boot-1.1.3-Fix-make-3.81-2.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

From Freescale ubootcpdref project plus Freescale patches

%Prep
%setup -n u-boot-1.1.3
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1 
%patch5 -p1 
%patch6 -p1 
%patch7 -p1 

%Build
PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-mpc7448hpc2_config}
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

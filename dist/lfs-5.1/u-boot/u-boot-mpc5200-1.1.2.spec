%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.1.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/System
Source          : u-boot-1.1.2.tar.bz2
Patch1		: u-boot-1.1.2-CVS-20050204.patch.bz2
Patch2		: u-boot-1.1.2-mpc5200.patch
Patch3		: u-boot-1.1.2-mpc5200-gcc343.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This specfile attempts to recreate the u-boot binaries
preinstalled on the Lite5200B and Media5200 platforms.

%Prep
%setup -n u-boot-1.1.2
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
export PATH=$UNSPOOF_PATH
PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-lite5200b_config}
make distclean
make $PKG_U_BOOT_CONFIG_TYPE
make CROSS_COMPILE=powerpc-603e-linux-

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
cp u-boot.bin $RPM_BUILD_ROOT/%{pfx}/boot
cp u-boot $RPM_BUILD_ROOT/%{pfx}/boot

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

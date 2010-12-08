%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : v1.3.0.rc3
Release         : 20071023
License         : GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Applications/System
Source          : u-boot-%{version}.tar.gz
Patch0          : u-boot-coldfire-fixes.patch
Patch1          : u-boot-v1.3.0.rc3-config.patch
Patch2          : u-boot-5373-updates.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Open source u-boot v1.3-rc3 plus Coldfire uClinux patches

%Prep
%setup -n u-boot
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
PKG_U_BOOT_CONFIG_TYPE=${SYSCFG_BOOT_CPU}
make distclean
make HOSTCC="$BUILDCC" CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_CONFIG_TYPE
make HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP" CROSS_COMPILE=$TOOLCHAIN_PREFIX

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

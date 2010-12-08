%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 1.2.0
Release         : 20070718
License         : GPL
Vendor          : Freescale
Packager        : Kurt Mahan
Group           : Applications/System
Source          : u-boot-1.2.0.tar.bz2
Patch0          : u-boot-1.2.0-d35b508a5-1.patch
Patch1          : u-boot-1.2.0-m5445x.patch 
Patch2          : u-boot-1.2.0-m5445x-atmel-jffs-offset.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Open source u-boot 1.2.0 plus Freescale patches

%Prep
%setup -n u-boot-1.2.0
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
PKG_U_BOOT_CONFIG_TYPE=${PKG_U_BOOT_CONFIG_TYPE:-MCF54455EVB_config}
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

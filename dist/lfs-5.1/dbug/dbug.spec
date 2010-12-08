%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define dversion dbug

Summary         : dBUG bootloader
Name            : dbug
Version         : 4
Release         : d
License         : Freescale EULA
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Applications/System
Source          : %{name}-%{version}.%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{dversion}

%Build
echo "Building dBUG for $SYSCFG_BOOT_CPU" 
make $SYSCFG_BOOT_CPU

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
cp -a obj/$SYSCFG_BOOT_CPU/gnu/${SYSCFG_BOOT_CPU}_flash.* $RPM_BUILD_ROOT/%{pfx}/boot/

%Clean
make ${SYSCFG_BOOT_CPU}-clean

%Files
%defattr(-,root,root)
%{pfx}/*


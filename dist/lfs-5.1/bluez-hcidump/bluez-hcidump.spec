%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : BlueZ bluetooth hcidump utility
Name            : bluez-hcidump
Version         : 1.29
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	--with-bluez=$DEV_IMAGE/usr/lib
make all

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make  install DESTDIR=${RPM_BUILD_ROOT}/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


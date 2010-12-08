%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : BlueZ bluetooth libraries
Name            : bluez-libs
Version         : 2.25
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch1          : bluez-libs-2.25-limits_h.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make all

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make install DESTDIR=${RPM_BUILD_ROOT}/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


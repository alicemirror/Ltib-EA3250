%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Event device test program
Name            : evtest
Version         : 1.23
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make 

%Install
install -d $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp evtest  $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

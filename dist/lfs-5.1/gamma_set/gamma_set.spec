%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Gamma Table Tweeker for ADS512101
Name            : gamma_set
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Martha Marx
Group           : Applications/Test
Source          : %{name}-%{version}-1.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : strongSwan is an OpenSource IPsec-based VPN Solution for Linux
Name            : strongswan
Version         : 4.2.8
Release         : 1
License         : GPL
Vendor          : strongSEC GmbH (http://www.strongsec.com)
Packager        : Lee Nipper
Group           : Applications/Internet
URL             : http://www.strongswan.org
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
./configure --prefix=%{_prefix} --sysconfdir=/etc --host=$CFGHOST
make 

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libxml++ is a C++ wrapper for the libxml2 XML parser library.
Name            : libxml++
Version         : 1.0.5
Release         : 1
License         : LGPL
Vendor          : ltib.org
Packager        : Mike Goins
Group           : Developmet/Libraries
URL             : http://libxmlplusplus.sourceforge.net/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
Requires        : libxml2

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" -exec rm -rf {} \;

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

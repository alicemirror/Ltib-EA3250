%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : JSON implementation in C.
Name            : json-c
Version         : 0.8
Release         : 1
License         : MIT
Vendor          : ltib.org
Packager        : Mike Goins
Group           : System Environment/Libraries
URL             : http://oss.metaparadigm.com/json-c/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

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
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

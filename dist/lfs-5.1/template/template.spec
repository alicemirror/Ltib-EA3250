%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Some simple but meaningful text
Name            : template
Version         : x.y
Release         : z
License         : xxxx
Vendor          : Freescale
Packager        : xxxx
Group           : xxxx
URL             : http://xxxx
Source          : %{name}-%{version}.tar.bz2
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

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

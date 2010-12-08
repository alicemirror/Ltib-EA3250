%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Templatized C++ Command Line Parser Library
Name            : tclap
Version         : 1.1.0
Release         : 1
License         : MIT
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
URL             : http://tclap.sourceforge.net/
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

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

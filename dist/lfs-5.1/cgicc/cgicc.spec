%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : GNU cgicc is a C++ class library for writing CGI applications
Name            : cgicc
Version         : 3.2.3
Release         : 1
License         : LGPL
Vendor          : Adtec, Inc.
Packager        : Mike Goins
Group           : Development/Libraries
URL             : http://www.gnu.org/software/cgicc/
Source          : %{name}-%{version}.tar.gz
Patch1          : cgicc-3.2.3-gcc4.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}


%Description
%{summary}

%Prep
%setup
%patch1 -p1

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

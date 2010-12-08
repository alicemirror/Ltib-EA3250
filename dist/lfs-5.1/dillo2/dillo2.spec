%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Dillo2 Web Browser 
Name            : dillo
Version         : 2.1 
Release         : 1
License         : GPL
Vendor          : Maxtrack
Packager        : Alan Carvalho, Hamilton Vera
Group           : Development/Libraries
URL             : http://www.dillo.org/
Source          : %{name}-%{version}.tar.bz2
Patch1          : dillo-2.1-cross.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --disable-efence --disable-gprof
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

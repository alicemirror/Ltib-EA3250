%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libXcursor cursor lib for X11 
Name            : libXcursor
Version         : 1.1.9
Release         : 1
License         : MIT
Vendor          : Maxtrack
Packager        : Alan Carvalho, Hamilton Vera
Group           : Development/Libraries
URL             : http://xorg.freedesktop.org/releases/individual/lib/
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
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

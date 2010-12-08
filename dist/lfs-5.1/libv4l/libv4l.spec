%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Video For Linux (V4L) library
Name            : libv4l
Version         : 0.6.0
Release         : 1
License         : LGPL
Vendor          : Maxtrack
Packager        : Alan Carvalho<alan@maxtrack.com.br>, Hamilton Vera<hamilton@maxtrack.com.br>, Rogerio Souza<rogerio@maxtrack.com.br>
Group           : System Environment/Libraries
URL             : http://freshmeat.net/projects/libv4l
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Libv4l is a collection of libraries that adds a thin abstraction layer on top of video4linux2 (V4L2) devices.

%Prep
%setup

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=/usr DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


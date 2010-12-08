%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : LibMatchBox
Name            : libmatchbox
Version         : 1.9
Release         : 1
License         : LGPL
Vendor          : Maxtrack
Packager        : Alan Carvalho<alan@maxtrack.com.br>, Hamilton Vera<hamilton@maxtrack.com.br>, Rogerio de Souza<rogerio@maxtrack.com.br>
Group           : Development/Libraries
URL             : http://matchbox-project.org/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
A small basic library that provides a large amount of shared functionality to the various matchbox librarys. Provides image processing, font abstraction, a tray app toolkit and more. It is licensed under LGPL.

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


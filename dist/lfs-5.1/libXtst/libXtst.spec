%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 libXtst runtime library
Name            : libXtst
Version         : 1.0.3
Release         : 1
License         : MIT
Vendor          : Maxtrack
Packager        : Alan Carvalho<alan@maxtrack.com.br>, Hamilton Vera<hamilton@maxtrack.com.br>, Rogerio de Souza<rogerio@maxtrack.com.br>
Group           : System Environment/Libraries
URL             : http://www.x.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
X.Org X11 libXtst runtime library

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --enable-malloc0returnsnull
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


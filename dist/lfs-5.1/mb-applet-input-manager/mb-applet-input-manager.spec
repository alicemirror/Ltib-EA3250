%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Input manager for the Matchbox Desktop
Name            : mb-applet-input-manager
Version         : 0.6
Release         : 1
License         : X11
Vendor          : Maxtrack
Packager        : Alan Carvalho<alan@maxtrack.com.br>, Hamilton Vera<hamilton@maxtrack.com.br>, Rogerio de Souza<rogerio@maxtrack.com.br>
Group           : Graphical desktop/Other
URL             : GPLv2+
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Input manager for the Matchbox Desktop.

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


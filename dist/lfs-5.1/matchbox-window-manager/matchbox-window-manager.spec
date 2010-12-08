%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : MatchBox Window Manager
Name            : matchbox-window-manager
Version         : 1.1
Release         : 1
License         : GPL
Vendor          : Maxtrack
Packager        : Alan Carvalho<alan@maxtrack.com.br>, Hamilton Vera<hamilton@maxtrack.com.br>, Rogerio de Souza<rogerio@maxtrack.com.br>
Group           : System/Libraries
URL             : http://matchbox-project.org/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
A pretty much unique X window manager with a classic PDA management policy. The most developed and mature Matchbox application.

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


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X Keyboard Configuration Database
Name            : xkeyboard-config
Version         : 1.6
Release         : 1
License         : MIT/X11
Vendor          : Maxtrack
Packager        : Rogerio de Souza<rogerio@maxtrack.com.br>
Group           : System/X11
URL             : http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
The non-arch keyboard configuration database for X Window System. The
goal is to provide the consistent, well-structured, frequently
released open source of X keyboard configuration data for X Window
System implementations (free, open source and commercial). The project
is targeted to XKB-based systems.

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


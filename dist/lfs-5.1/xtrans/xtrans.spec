%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Xtrans
Name            : xtrans
Version         : 1.2
Release         : 1
License         : X11
Vendor          : X.Org Foundation
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.x.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
xtrans is a library of code that is shared among various X packages to handle
network protocol transport in a modular fashion, allowing a single place to
add new transport types.   It is used by the X server, libX11, libICE, the
X font server, and related components.

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


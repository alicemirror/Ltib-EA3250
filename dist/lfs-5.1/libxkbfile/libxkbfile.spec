%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Lib xkbfile
Name            : libxkbfile
Version         : 1.0.5
Release         : 1
License         : X11
Vendor          : X.Org Foundation
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.x.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires	: libX11 libXdmcp

%Description
libxkbfile provides an interface to read and manipulate description files for XKB, the X11 keyboard configuration extension.

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


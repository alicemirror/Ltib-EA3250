%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Library for manipulating GIF format image files
Name            : giflib
Version         : 4.1.6
Release         : 1
License         : MIT
Vendor          : ltib.org
Packager        : Mike Goins
Group           : System Environment/Libraries
URL             : http://sourceforge.net/projects/giflib/
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
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

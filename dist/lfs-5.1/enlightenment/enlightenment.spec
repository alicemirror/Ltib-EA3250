%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Enlightenment 17
Name            : enlightenment
Version         : 0.16.999.050
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
Patch1          : enlightenment-0.16.999.050-host_name_max.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : ecore efreet embryo eet edje evas libXext libX11

%Description
The Enlightenment 0.17.0 window manager, development version.

%Prep
%setup
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --with-edje-cc=edje_cc --with-eet-eet=eet
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


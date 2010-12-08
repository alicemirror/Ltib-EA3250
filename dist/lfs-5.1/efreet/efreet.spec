%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Efreet
Name            : efreet
Version         : 0.5.0.050
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
Patch1          : efreet-0.5.0.050-host_name_max.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : ecore

%Description
An implementation of several specifications from freedesktop.org intended for use in Enlightenment DR17 (e17) and other applications using the Enlightenment Foundation Libraries (EFL). Currently, the following specifications are included:
  o Base Directory
  o Desktop Entry
  o Icon Theme
  o Menu

%Prep
%setup
%patch1 -p1

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


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Light Media Scanner
Name            : lightmediascanner
Version         : 0.2.0.0
Release         : 1
License         : BSD
Vendor          : ProFUSION embedded systems <contact@profusion.mobi>
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://lms.garage.maemo.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : evas edje ecore

%Description
Light Media Scanner

%Prep
%setup

%Build
SQLITE3_CFLAGS="-I$DEV_IMAGE/usr/include" SQLITE3_LIBS="-L$DEV_IMAGE/usr/lib/ $DEV_IMAGE/usr/lib/libsqlite3.so" ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} 
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


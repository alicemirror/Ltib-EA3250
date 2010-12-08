%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Lib Pthread-stubs
Name            : libpthread-stubs
Version         : 0.1
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
This library provides weak aliases for pthread functions not provided in libc
or otherwise available by default.  Libraries like libxcb rely on pthread
stubs to use pthreads optionally, becoming thread-safe when linked to
libpthread, while avoiding any performance hit when running single-threaded.


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


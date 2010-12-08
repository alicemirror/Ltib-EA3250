%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Lightweight C library that eases the writing of UNIX daemons.
Name            : libdaemon
Version         : 0.13
Release         : 1
License         : LGPL
Vendor          : ltib.org
Packager        : Mike Goins
Group           : System Environment/Libraries
URL             : http://0pointer.de/lennart/projects/libdaemon/
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
env ac_cv_func_setpgrp_void=yes \
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

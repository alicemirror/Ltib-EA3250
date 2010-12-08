%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A command line tool for transferring files with URL syntax.
Name            : curl
Version         : 7.16.2
Release         : 1
License         : MIT License
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
URL             : http://curl.haxx.se
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --with-random=/dev/urandom
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

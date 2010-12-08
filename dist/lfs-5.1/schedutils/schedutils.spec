%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for manipulating process scheduler attributes.
Name            : schedutils
Version         : 0.7.2
Release         : 1
License         : BSD License
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make HOSTCC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr
for i in bin sbin
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/$i
done
install -m 555 getsched  $RPM_BUILD_ROOT/%{pfx}/usr/bin
install -m 544 resched $RPM_BUILD_ROOT/%{pfx}/usr/sbin
install -m 544 sched $RPM_BUILD_ROOT/%{pfx}/usr/sbin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

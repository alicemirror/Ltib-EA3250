%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : TTY mode communications package ala Telix
Name            : minicom
Version         : 2.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Umesh Nerlige
Group           : Applications/Communications
URL             : http://ftp.debian.org/debian/pool/main/m/minicom/minicom_2.2.orig.tar.gz
Source          : %{name}_%{version}.orig.tar.gz
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

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

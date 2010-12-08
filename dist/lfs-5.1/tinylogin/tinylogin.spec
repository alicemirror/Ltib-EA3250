%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A small package that replaces getty and friends
Name            : tinylogin
Version         : 1.4
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
Source          : http://tinylogin.busybox.net/downloads/tinylogin-1.4.tar.bz2
Patch0          : tinylogin.tiocspgrp.patch
Patch1          : tinylogin-1.4-noroot.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1


%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT/%{pfx} install


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%attr(4755, root, -) %{pfx}/bin/tinylogin
%{pfx}/*

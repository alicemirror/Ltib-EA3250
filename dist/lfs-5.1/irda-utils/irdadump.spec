%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for debugging infrared communication between devices
Name            : irdadump
Version         : 0.9.18
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System/Servers
Source          : irda-utils-%{version}.tar.gz
Patch1          : irda-utils-%{version}-irdadump-hinko.patch
URL             : http://sourceforge.net/projects/irda
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This spec file only builds irdadump from irda-utils

%Prep
%setup -n irda-utils-%{version}
%patch1 -p1

%Build
make -C irdadump SYS_INCLUDES= SYS_LIBPATH= CC=gcc LD=ld

%Install
rm -rf $RPM_BUILD_ROOT
make -C irdadump install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root,0755)
%{pfx}/*

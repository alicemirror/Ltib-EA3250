%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for managing processes on your system
Name            : psmisc
Version         : 22.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : psmisc-%{version}.tar.gz
Patch1          : psmisc-22.3-intl.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
CC=gcc ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir} -C
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 DESTDIR=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : PCI bus related utilities.
Name            : pciutils
Version         : 2.1.11
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
perl -pi -e 's,cpu=`uname.*$,cpu='${LINTARCH}',' lib/configure
make -j1 PREFIX=%{_prefix}

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \
             MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

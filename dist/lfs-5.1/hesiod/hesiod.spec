%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Hesiod libraries and sample programs.
Name            : hesiod
Version         : 3.0.2
Release         : 1
License         : Internet Systems Consortium (distributable)
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
LIBS="-lresolv" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make all

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \
             MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

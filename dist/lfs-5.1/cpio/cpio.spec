%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A GNU archiving program.
Name            : cpio
Version         : 2.6
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
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
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \
             MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

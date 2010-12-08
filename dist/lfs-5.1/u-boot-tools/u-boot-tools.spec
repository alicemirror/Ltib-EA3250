%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader tools
Name            : u-boot-tools
Version         : 1.1.6
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch1          : u-boot-tools-1.1.6-make_env.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}


%Prep
%setup
%patch1 -p1

%Build
BUILDCC=gcc
BUILDSTRIP=strip
make -C tools HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
make -C tools DESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

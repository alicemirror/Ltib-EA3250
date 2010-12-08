%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utility for creating romfs filesystems
Name            : genromfs
Version         : 0.5.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
Patch1          : genromfs-0.5.1-make.patch
Patch2          : genromfs-0.5.1-adddot.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make prefix=%{_prefix}

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make install prefix=%{_prefix} PREFIX=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

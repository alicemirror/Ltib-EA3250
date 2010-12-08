%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : MCF54455 Demonstration package
Name            : mcf54455-demo
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Yaroslav Vinogradov
Group           : System Environment/Utilities
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build

%Install
mkdir -p $RPM_BUILD_ROOT/%{pfx}
cp -a * $RPM_BUILD_ROOT/%{pfx}

%Clean


%Files
%defattr(-,root,root)
%{pfx}/*

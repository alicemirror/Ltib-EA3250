%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : i.MX31 ADS TV-Out test package
Name            : tvout-test-mx31
Version         : 1.1
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Quinn Jensen
Group           : Applications/Test
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/tvout-test-mx31
cp -ar * $RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

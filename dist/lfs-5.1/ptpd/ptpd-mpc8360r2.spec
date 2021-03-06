%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Implement the Precision Time protocol (PTP) as defined by the IEEE 1588 standard.
Name            : ptpd
Version         : 1b4
Release         : 1
License         : BSD License
Vendor          : Freescale
Packager        : Jerry Huang
Group           : Applications/System
Source          : %{name}_%{version}.tar.gz
Patch0          : ptpd-mpc8360r2.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n ptpd
%patch0 -p1

%Build
make -C src

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin

cp -f src/ptpd $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

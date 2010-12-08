%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : VIU driver test tool
Name            : viutest
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Chen Hongjun
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp vcat viutest.sh $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

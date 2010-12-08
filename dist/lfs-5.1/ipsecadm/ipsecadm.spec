%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : ipsecadm ipsec_tunnel administration
Name            : ipsecadm
Version         : 0.9
Release         : pre1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-0.9-pre.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n ipsecadm

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
cp -a ipsecadm $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/ipsecadm

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

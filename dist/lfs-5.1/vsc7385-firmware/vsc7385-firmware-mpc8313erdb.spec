%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Firmware image for the VSC7385
Name            : vsc7385-firmware
Version         : 2.0
Release         : 1
License         : Freescale EULA
Vendor          : Freescale
Packager        : Vivienne Li
Group           : Development/Debuggers
Source          : %{name}-mpc8313erdb-2.tgz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Binary only package.

%Prep
%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/lib/firmware
cp vsc2bin $RPM_BUILD_ROOT/%{pfx}/lib/firmware/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

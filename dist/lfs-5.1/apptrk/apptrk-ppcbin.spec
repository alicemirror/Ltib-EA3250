%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Userspace debug agent for Codewarrior
Name            : apptrk
Version         : 1.37
Release         : 1
License         : Freescale EULA
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Debuggers
Source          : AppTRK-1.37.tgz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Binary only package.

%Prep
%setup -n AppTRK-1.37

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp AppTRK.elf $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
chmod +x $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
cp AppTRK_debug.elf $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk_debug
chmod +x $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk_debug

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

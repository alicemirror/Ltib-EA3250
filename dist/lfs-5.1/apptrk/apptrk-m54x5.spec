%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Apptrk - M54X5 target executable for Codewarrior
Name            : AppTrk-m54x5
Version         : 1.37
Release         : 1
License         : Freescale EULA
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Development/Debuggers
Source          : %{name}-%{version}.%{release}.tar.gz
BuildRoot       : %{_tmppath}/AppTrk-m54x5-1.37
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
if [ $TOOLCHAIN_PREFIX = "m68k-linux-" ]
then
    # This binary was compiled for the old 3.4 toolchain
    cp AppTrk_mcf5475_5485_rel.elf $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
else
    # This binary was compiled for the new CodeSourcery 4.1 toolchain
    cp AppTrk_mcf5475_5485_rel_2.3.elf $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Apptrk - target executable for Codewarrior
Name            : AppTrk-m68k
Version         : 1.42
Release         : 0
License         : Freescale EULA
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Development/Debuggers
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/MetroTRK
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
if echo ${PLATFORM} | grep -q 'm53'
then
   echo "Installing binary for Coldfire V3 core processor"
   cp v3-bin/AppTrk_CORE_v3_rel.bin $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
   chmod 755 $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
else
if echo ${PLATFORM} | grep -q 'm5253'
then
   echo "Installing binary for Coldfire m5253 core processor"
   cp v2-5253-bin/AppTrk_CORE_5253_rel.bin $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
   chmod 755 $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
else
if echo ${PLATFORM} | grep -q 'm52'
then
   echo "Installing binary for Coldfire V2 core processor"
   cp v2-bin/AppTrk_CORE_v2_rel.bin $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
   chmod 755 $RPM_BUILD_ROOT/%{pfx}/usr/bin/apptrk
else
   echo "No Apptrk binary found for this Coldfire core"
fi
fi
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

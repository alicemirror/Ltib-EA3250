%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Freescale TLU test package
Name            : fsl_tlu
Version         : 1.0.0
Release         : alpha5
License         : Freescale EULA
Vendor          : Freescale
Packager        : Haiying Wang
Group           : Development/Debuggers
Source          : %{name}-%{version}-%{release}-2.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build

%Install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/fsl_tlu
cp * $RPM_BUILD_ROOT/%{pfx}/fsl_tlu

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
                  

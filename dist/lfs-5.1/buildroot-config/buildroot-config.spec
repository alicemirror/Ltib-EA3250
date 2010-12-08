%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Linux kernel configuration language parser (busybox style)
Name            : buildroot-config
Version         : 1.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make conf mconf

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp -a conf mconf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



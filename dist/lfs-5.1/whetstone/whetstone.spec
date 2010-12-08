%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Floating point test package
Name            : whetstone
Version         : 1.0
Release         : 1
License         : Not Distributable
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : Applications/Test
Source          : %{name}-%{version}.tar.bz2
Patch1          : whetstone-1.0-loopcal.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
gcc -O3 -o whetstone whetstone.c -lm

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/{bin,src/whetstone}
cp whetstone $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp whetstone.c $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/src/whetstone

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


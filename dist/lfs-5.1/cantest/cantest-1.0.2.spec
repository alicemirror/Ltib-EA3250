%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : cantest
Name            : cantest
Version         : 1.0
Release         : 2
License         : GPL
Vendor          : Freescale
Packager        : Chen Hongjun
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0		: cantest-1.0.patch
Patch1          : cantest-1.0-uClinux.patch
Patch2          : cantest-1.0-cansend-1.patch
Patch3          : cantest-1.0-cansend-debug.patch
Patch4          : cantest-1.0.2-update.patch
Patch5          : cantest-1.0.2-mask-id.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://svn.berlios.de/svnroot/repos/socketcan/trunk/can-utils/

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp cantest $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

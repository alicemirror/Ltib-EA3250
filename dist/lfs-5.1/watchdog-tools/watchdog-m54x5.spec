%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Watchdog timer setup test and example code
Name            : watchdog
Version         : 1.1
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Development/Tools
Source          : watchdog-%{version}.tar.gz
Patch1          : watchdog-1.1-fixups2.patch
Patch2          : watchdog-1.2-4.2-fixups.patch
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
Example code used for validation of the M5475/M5485 watchdog device driver.

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/root
install -m 755 watchdog $RPM_BUILD_ROOT/%{pfx}/root/watchdog

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

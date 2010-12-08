%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : DSPI test and example code
Name            : dspi
Version         : 1.1
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Development/Tools
Source          : dspi-%{version}.tar.gz
Patch1          : dspi-1.1-fixups1.patch
Patch2          : dspi-1.1-4.2-fixups.patch
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
Example code used for validation of the M5475/M5485 dspi device
driver.

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
install -m 755 dspi_read $RPM_BUILD_ROOT/%{pfx}/usr/bin/dspi_read
install -m 755 dspi_write $RPM_BUILD_ROOT/%{pfx}/usr/bin/dspi_write

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

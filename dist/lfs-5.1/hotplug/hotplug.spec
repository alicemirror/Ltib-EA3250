%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A helper application which loads modules for USB devices
Name            : hotplug
Version         : 2004_03_29
Release         : 3
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Kernel
Source          : %{name}-%{version}.tar.gz
Patch1          : hotplug-2004_03_29-initd.patch
Patch2          : hotplug-2004_03_29-dash.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(755,root,root)  %{pfx}/var/run/usb
%{pfx}/*

%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Device files for a small embedded system
Name            : dev
Version         : 1.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
#BuildRequires   : rpm > 4.0.3

%Description
%{summary}

Notes:

 * Uses device_table.txt (genext2fs) as an input file
 * Not needed if you using devfs or udev
 * needs RPM 4.0.3-0.71 or higher

%Prep
%setup -n %{name}-%{version}

%Build

%Install
rm -rf $RPM_BUILD_ROOT
if [ -f "$TOP/bin/device_table.txt" ]
then
    DEV_TABLE="$TOP/bin/device_table.txt"
else
    DEV_TABLE=device_table.txt
fi
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/dev
ln -s /var/tmp/log $RPM_BUILD_ROOT/%{pfx}/%{base}/dev/log
ln -s /proc/mounts $RPM_BUILD_ROOT/%{pfx}/%{base}/dev/mtab
PREFIX=%{pfx}/%{base} perl mkrpmdev $DEV_TABLE > /tmp/manifest

%Clean
rm -rf $RPM_BUILD_ROOT
rm -f /tmp/manifest

%Files -f /tmp/manifest
%defattr(-,root,root)
%{pfx}/*

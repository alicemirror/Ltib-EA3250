%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Displays serial port modem status lines
Name            : statserial
Version         : 1.1
Release         : 22
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/Test
Source          : statserial_1.1.orig.tar.gz
Patch1		: statserial_1.1-22.diff.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n statserial-1.1.orig
%patch1 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
install -m 555 statserial -p $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Used to start apptrk as a deamon
Name            : daemonizer
Version         : 1.0
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Development/Debuggers
Source          : daemonizer-1.0.tar.gz
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
Starting apptrk using the daemonizer allows to run and
debug applications from codewarrior without having to login
into the target and to start apptrk manually.

%Prep
%setup

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
install -m 755 daemon $RPM_BUILD_ROOT/%{pfx}/usr/bin/daemon

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

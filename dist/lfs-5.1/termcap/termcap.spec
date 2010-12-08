%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : minimal /etc/termcap needed by minicom etc
Name            : termcap
Version         : 1.2
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
URL             : ftp://ftp.au.netbsd.org/pub/NetBSD/NetBSD-current/src/distrib/sparc64/instfs/termcap.mini
Source          : %{name}-mini-%{version}.tar.gz
Patch1          : termcap-1.2-vt102.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-mini-%{version}
%patch1 -p1

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
cp termcap.mini $RPM_BUILD_ROOT/%{pfx}/etc/termcap

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

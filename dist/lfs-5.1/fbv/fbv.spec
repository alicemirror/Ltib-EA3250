%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : FrameBuffer Viewer
Name            : fbv
Version         : 1.0b
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Chen Hongjun
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0		: fbv-multi-planes.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://s-tech.elsat.net.pl/fbv/

%Description
Fbv 1.0b plus freescale patch that adde multi plane support.

%{summary}

%Prep
%setup
%patch0 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp fbv $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

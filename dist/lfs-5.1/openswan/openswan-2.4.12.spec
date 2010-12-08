%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Openswan is an Open Source implementation of IPsec for the Linux operating system. Is it a code fork of the FreeS/WAN project, started by a few of the developers who were growing frustrated with the politics surrounding the FreeS/WAN project.
Name            : openswan
Version         : 2.4.12
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Xianghua Xiao
Group           : Applications/Internet
Source          : %{name}-%{version}.tar.gz
Patch0          : openswan-2.4.12-make-fixes.patch
Patch1          : openswan-2.4.12.patch
Patch2          : openswan-2.4.12-hdrdir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
make -j1 HOSTCC="$BUILDCC" KERNELSRC=$RPM_BUILD_DIR/linux-2.6.24 programs

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install FINALSBINDIR=/usr/sbin DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(744,root,root) %{pfx}/etc/ipsec.d/private
%attr(744,root,root) %{pfx}/var/run/pluto
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Tools for managing kernel packet filtering capabilities
Name		: iptables
Version		: 1.4.2
Release		: 1
License		: GPL
Vendor		: Freescale
Packager	: Stuart Hughes, Emil Medve
Group		: System Environment/Base
URL		: http://www.netfilter.org/projects/iptables
Source		: %{name}-%{version}.tar.bz2
Patch0		: userspace-iptables-1.4.2-l7pme-1.patch
Patch1		: iptables-1.4.2-libxt_TOS.patch
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

iptables is the userspace command line program used to configure the Linux
2.4.x and 2.6.x IPv4 packet filtering ruleset. It is targeted towards system
administrators

Since Network Address Translation is also configured from the packet filter
ruleset, iptables is used for this, too

The iptables package also includes ip6tables. ip6tables is used for configuring
the IPv6 packet filter

iptables requires a kernel that features the ip_tables packet filter. This
includes all 2.4.x and 2.6.x kernel releases

Main Features
		* listing the contents of the packet filter ruleset
		* adding/removing/modifying rules in the packet filter ruleset
		* listing/zeroing per-rule counters of the packet filter ruleset

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

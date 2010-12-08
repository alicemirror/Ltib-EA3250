%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The conntrack-tools are a set of tools targeted at system administrators. They are conntrack, the userspace command line interface, and conntrackd, the userspace daemon
Name            : conntrack-tools
Version         : 0.9.4
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Emil Medve
Group           : System Environment/Base
URL             : http://www.netfilter.org/projects/conntrack-tools
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

The tool conntrack provides a full featured interface that is intended to replace the old
/proc/net/ip_conntrack interface. Using conntrack, you can view and manage the in-kernel connection
tracking state table from userspace. On the other hand, conntrackd covers the specific aspects of
stateful firewalls to enable highly available scenarios, and can be used as statistics collector as
well

conntrack-tools requires libnetfilter_conntrack, libnfnetlink and a kernel that features the
netnetlink_conntrack subsystem. For officially released kernels, this means 2.6.14, but we suggest
you to use 2.6.18 or later

Main Features
    * listing the contents of the conntrack table
    * searching for individual entries in the conntrack table
    * adding new entries to the conntrack table
    * listing entries in the expect table
    * adding new entries to the expect table

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/%{name}/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

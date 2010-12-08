%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libnfnetlink is the low-level library for netfilter related kernel/userspace communication
Name            : libnfnetlink
Version         : 0.0.25
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Emil Medve
Group           : System Environment/Base
URL             : http://www.netfilter.org/projects/libnfnetlink
Patch0          : %{name}-%{version}-linux_types_h.patch
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}
libnfnetlink is the low-level library for netfilter related kernel/userspace communication. It
provides a generic messaging infrastructure for in-kernel netfilter subsystems (such as
nfnetlink_log, nfnetlink_queue, nfnetlink_conntrack) and their respective users and/or management
tools in userspace

This library is not meant as a public API for application developers. It is only used by other
netfilter.org projects, such as libnetfilter_log, libnetfilter_queue or libnetfilter_conntrack

libnfnetlink requires and a kernel that features the nfnetlink subsystem. This includes all 2.6.x
kernels >= 2.6.14

Main features
    * low-level nfnetlink message processing functions

%Prep
%setup
%patch0 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/%{name}.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

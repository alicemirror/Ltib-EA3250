%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libnetfilter_conntrack is a userspace library providing a programming interface (API) to the in-kernel connection tracking state table
Name            : libnetfilter_conntrack
Version         : 0.0.80
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Emil Medve
Group           : System Environment/Base
URL             : http://netfilter.org/projects/libnetfilter_conntrack
Source          : %{name}-%{version}.tar.bz2
Patch1          : libnetfilter_conntrack-0.0.80-relink.patch
Patch2          : libnetfilter_conntrack-0.0.80-glibc-2.8.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

libnetfilter_conntrack has been previously known as libnfnetlink_conntrack and libctnetlink

libnetfilter_conntrack is used by conntrack

libnetfilter_conntrack requires libnfnetlink and a kernel that includes the nfnetlink_conntrack
subsystem (i.e. 2.6.14 or later)

Main features
    * listing/retrieving entries from the kernel connection tracking table
    * inserting/modifying/deleting entries from the kernel connection tracking table
    * listing/retrieving entries from the kernel expect table
    * inserting/modifying/deleting entries from the kernel expect table

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/%{name}.la   \
       $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/%{name}/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

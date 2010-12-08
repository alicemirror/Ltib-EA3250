%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A tool for managing Soft RAID under Linux
Name            : mdadm
Version         : 2.3.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Michael Barkowski
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
# the CXFLAGS clause is to fix gcc-3.3.2 era compilers.  Not the compilers
# fault, but the package includes byteorder stuff in a weird way that
# means this flag which should be set is not.
# removed -Werror from CWFLAGS as gcc-4.1.1 will throw up warnings
make CC=gcc CXFLAGS=-D__BYTEORDER_HAS_U64__ CWFLAGS="-Wall -Wstrict-prototypes"

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

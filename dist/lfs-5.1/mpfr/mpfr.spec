%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Multiple-precision floating-point library.
Name            : mpfr
Version         : 2.3.2
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
The MPFR library is a C library for multiple-precision floating-point
computations with correct rounding.  The main goal of MPFR is to provide a
library for multiple-precision floating-point computation which is both
efficient and has a well-defined semantics. 

%Prep
%setup 

%Build
CC_FOR_BUILD="${BUILDCC}" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make


%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

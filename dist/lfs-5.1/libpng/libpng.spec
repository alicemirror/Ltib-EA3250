%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library of functions for manipulating PNG image format files
Name            : libpng
Version         : 1.2.8
Release         : 1
License         : distributable, OSI approved
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
Patch1          : libpng-1.2.8-link_to_proper_libs-1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
make prefix=%{_prefix} -f scripts/makefile.linux

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix} 
make prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} install -f scripts/makefile.linux

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


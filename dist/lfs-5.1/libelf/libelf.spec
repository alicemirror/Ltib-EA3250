%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : An ELF object file access library
Name            : libelf
Version         : 0.8.5
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
if [ "$GNUTARCH" = m68knommu ]
then
mr_cv_target_elf=yes \
./configure --prefix=%{_prefix} --disable-shared
else
mr_cv_target_elf=yes \
./configure --prefix=%{_prefix}
fi
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install instroot=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

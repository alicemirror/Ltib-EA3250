%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : language and system independent CORBA interfaces for creating reusable components and compound documents
Name            : libbonobo
Version         : 2.6.0
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
License         : LGPL/GPL
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

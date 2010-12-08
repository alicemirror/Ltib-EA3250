%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define pkg_name libIDL

Summary         : Corba Interface Definition Language interface files
Name            : libidl
Version         : 0.8.3
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          : %{pkg_name}-%{version}.tar.bz2
License         : LGPL
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup -n %{pkg_name}-%{version}

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

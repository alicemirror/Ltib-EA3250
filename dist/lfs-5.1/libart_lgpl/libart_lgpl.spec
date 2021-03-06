%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libart_lgpl library is used as the anti-aliased render engine for libgnomecanvas.
Name            : libart_lgpl
Version         : 2.3.16
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
License         : LGPL
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

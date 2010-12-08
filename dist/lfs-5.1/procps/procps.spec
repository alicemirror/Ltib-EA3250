%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : System and process monitoring utilities
Name            : procps
Version         : 3.2.7
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
make -j1 CPPFLAGS= m64= lib64=

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 DESTDIR=$RPM_BUILD_ROOT/%{pfx} lib=$RPM_BUILD_ROOT/%{pfx}/usr/lib/ install="install -D" install ldconfig="" SKIP='$(bin)kill $(man1)kill.1'

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



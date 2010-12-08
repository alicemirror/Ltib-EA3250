%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Bridge Utilities
Name            : bridge-utils
Version         : 1.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Lee Nipper
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://linux-net.osdl.org/index.php/Bridge

%Description
%{summary}

Note: requires the following kernel config option:
CONFIG_BRIDGE

%Prep
%setup 

%Build
autoconf
./configure --host=$CFGHOST --exec-prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

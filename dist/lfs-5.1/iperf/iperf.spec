%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : iperf is a tool to measure IP bandwidth using UDP or TCP
Name            : iperf
Version         : 1.7.0
Release         : 1
License         : Distributable/GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}-source.tar.gz
Patch1          : iperf-1.7.0-vfork.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://dast.nlanr.net/Projects/Iperf/

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
cd cfg
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} 
cd -
make

%Install
rm -rf $RPM_BUILD_ROOT
cd src
make install INSTALL_DIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cd -

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

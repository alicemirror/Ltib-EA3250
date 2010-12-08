%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : An Implementation of the RFC1413 Identification Server
Name            : pidentd
Version         : 3.0.19
Release         : 1
License         : Freely Distributable
Vendor          : Freescale
Packager        : John Rigby/Steve Papacharalambous
Group           : System Environment/Daemons
URL             : ftp://ftp.lysator.liu.se/pub/ident/servers/pidentd-3.0.19.tar.gz
Source          : %{name}-%{version}.tar.gz
Patch0          : pidentd-3.0.19-crossbuild.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1

%Build
ac_cv_have_ipv6=yes ./configure --prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install mandir=$RPM_BUILD_ROOT/%{pfx}/usr/share/man

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

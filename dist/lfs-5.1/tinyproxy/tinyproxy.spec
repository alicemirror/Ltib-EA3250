%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Lightweight HTTP/SSL proxy
Name            : tinyproxy
Version         : 1.6.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/Internet
URL             : http://sourceforge.net/projects/tinyproxy
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
if [ -n "${UCLIBC}" ]
then
    config_opts='LDFLAGS=-lintl'
fi

eval ${config_opts} \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(644,root,root)  %{pfx}/etc/tinyproxy/tinyproxy.conf
%attr(644,root,root)  %{pfx}/etc/tinyproxy/tinyproxy.conf-dist
%{pfx}/*

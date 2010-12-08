%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A network traffic monitoring tool
Name            : tcpdump
Version         : 3.8.3
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Internet
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
# I don't think the actual kernel version matters.
ac_cv_linux_vers=2 \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --config-cache --mandir=%{_mandir} --without-crypto
make INCLS="-I. -I./missing" LDFLAGS=

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Internet Systems Consortium BIND DNS server, resolver, and tools.
Name            : bind
Version         : 9.3.2
Release         : 1
License         : Internet Systems Consortium (distributable)
Vendor          : Freescale
Packager        : John Faith
Group           : Applications/Internet
Source          : bind-9.3.2.tar.gz
Patch1          : bind-9.3.2-sip.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://www.isc.org/sw/bind/

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --with-randomdev=/dev/random
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


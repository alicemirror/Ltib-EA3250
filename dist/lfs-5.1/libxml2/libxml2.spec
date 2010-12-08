%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Libraries, includes, etc. to develop XML/HTML applications
Name		: libxml2
Version		: 2.7.2
Release		: 0
Vendor		: Freescale
Packager	: Jason Jin, Stuart Hughes, Kurt Mahan, Emil Medve
Group		: Development/Libraries
URL		: http://www.xmlsoft.org
Source		: %{name}-%{version}.tar.gz
License		: MIT
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --with-history --without-python
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" -exec rm -rf {} \;

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-, root, root)
%{pfx}/*

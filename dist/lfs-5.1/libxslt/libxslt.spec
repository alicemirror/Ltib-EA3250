%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Library providing XSLT support (convert xml -> html etc)
Name            : libxslt
Version         : 1.1.11
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
License         : MIT
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --without-crypto

# Avoid libtool searching in /usr/lib
perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

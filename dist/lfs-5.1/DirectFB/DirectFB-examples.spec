%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A set of simple DirectFB applications for testing and demonstration purposes
Name            : DirectFB-examples
Version         : 0.9.23
Release         : 1
License         : MIT
Vendor          : Freescale
Packager        : WMSG
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
export PKG_CONFIG_PATH=$DEV_IMAGE/%{_prefix}/lib/pkgconfig
export DIRECTFB_CFLAGS="-D_REENTRANT -D_GNU_SOURCE -I$DEV_IMAGE/%{_prefix}/include/directfb"
./configure --enable-shared --host=$CFGHOST --build=%{_build} --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

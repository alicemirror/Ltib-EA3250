%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Linux USB utilities
Name            : usbutils
Version         : 0.70
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : libusb

%Description
%{summary}

%Prep
%setup 

%Build
ac_cv_func_malloc_0_nonnull=yes \
  CC=gcc ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
         --config-cache --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

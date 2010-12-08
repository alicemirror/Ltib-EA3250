# Template = kernel-common.tmpl

%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define dversion 2.8.18
%define pkg_name xfsprogs
%define release 1

Summary         : XFS utilities
Name            : xfs
Version         : 2.8.18
Release         : 1
License         : GPL
Vendor          : Open source
Packager        : Michael Reiss
Group           : System Environment/Kernel
Source          : %{pkg_name}-%{dversion}-%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{pkg_name}-%{dversion}

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} PLATFORM=linux
make

%Install
DIST_ROOT=$RPM_BUILD_ROOT/%{pfx}
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV
make install DIST_MANIFEST=$DIST_INSTALL
make -C build/rpm rpmfiles DIST_MANIFEST=$DIST_INSTALL
make install-dev DIST_MANIFEST=$DIST_INSTALL_DEV
make -C build/rpm rpmfiles-dev DIST_MANIFEST=$DIST_INSTALL_DEV

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

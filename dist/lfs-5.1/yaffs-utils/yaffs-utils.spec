%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : YAFFS Utilities.
Name            : yaffs_utils
Version         : 20060418
Release         : 3
License         : GPL
Vendor          : Freescale
Packager        : Alan Tull
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0          : yaffs_mxc.patch
Patch1          : yaffs_utils-20060418-mtd-include.patch
Patch2          : yaffs_utils-20060418-include-order.patch
Patch3          : yaffs_utils-20060418-mkyaffs2image.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Extracted from the cvs at www.aleph1.co.uk/yaffs


%Prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
make KERNELDIR=$DEV_IMAGE/usr/src/linux -C yaffs2/utils

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
make -j1 -C yaffs2/utils DESTDIR=$RPM_BUILD_ROOT/%{pfx} SBINDIR=%{_prefix}/bin install

%Clean
rm -rf $RPM_BUILD_ROOT
make -C yaffs/utils clean

%Files
%defattr(-,root,root)
%{pfx}/*

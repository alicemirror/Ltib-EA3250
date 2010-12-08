%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Wan Gateway Kernel Module
Name            : wangw
Version         : 1.0.4
Release         : 1
License         : Freescale Internal Use Only
Vendor          : Freescale
Packager        : Lee Nipper
Group           : System Environment/Kernel
Source          : %{name}-%{version}.tar.gz
Patch0          : wangw-1.0.4-toolchain.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This package contains the kernel module for the
Wang Gateway Interworking and Termination Driver
developed by Freescale Romania.

Notes:

You need to have a built unpacked kernel source tree available
via $RPM_BUILD_DIR/linux.

We build spoofed, so gcc == the cross compiler

%Prep
%setup
%patch0 -p1

%Build
if [ ! -f $RPM_BUILD_DIR/linux/Makefile ]
then
    cat <<TXT
You need a built unpacked kernel source tree in:
$RPM_BUILD_DIR/linux/Makefile
to build kernel modules
TXT
    exit 1
fi

TOPDIR=`pwd`/NetCommSw/build/linux_2.6_836x_gcc_build
TOPLINUX=$RPM_BUILD_DIR/linux

(cd $TOPDIR; make wangw.ko COMPILER=   TOPDIR=$TOPDIR TOPLINUX=$TOPLINUX)

%Install
rm -rf $RPM_BUILD_ROOT
KVER="`perl -e '$/ = ""; $_ = <>; m,VERSION\s*=\s*(\d)\s*PATCHLEVEL\s*=\s*(\d+)\s*SUBLEVEL\s*=\s*(\d+)\s*,ms; print  "$1.$2.$3$4"' $RPM_BUILD_DIR/linux/Makefile`"
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/swang/
TOPDIR=`pwd`/NetCommSw/build/linux_2.6_836x_gcc_build
cp $TOPDIR/*.ko $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/swang/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

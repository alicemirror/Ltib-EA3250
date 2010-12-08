%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Small Wan Gateway Proof of Concept Software
Name            : swang-poc
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Lee Nipper
Group           : Applications/Test
Source          : %{name}-%{version}.tar.gz
Patch0          : swang-poc-1.0-fix-install.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This package includes the applications and kernel modules for
the Wan Gateway Proof-of-Concept Demonstration S/W.
The purpose of this software is to demonstrate port-to-port
forwarding by lower level hardware which supports port interworking.

This software makes use of an older version of the conntrack-tools from
this location: 
http://www.netfilter.org/projects/conntrack-tools/index.html

Notes:

You need to have a built unpacked kernel source tree available
via $RPM_BUILD_DIR/linux.

We build spoofed, so gcc == the cross compiler

%Prep
%setup
%patch0 -p0

%Build
# Build the kernel modules first
if [ ! -f $RPM_BUILD_DIR/linux/Makefile ]
then
    cat <<TXT
You need a built unpacked kernel source tree in:
$RPM_BUILD_DIR/linux/Makefile
to build kernel modules
TXT
    exit 1
fi

(cd kernel/ipc; make KERNELDIR=$RPM_BUILD_DIR/linux)
(cd kernel/iptables_fsl; make KERNELDIR=$RPM_BUILD_DIR/linux)

# Build the applications
(cd applications/conntrack; make)
(cd applications/ipdaemon; make)

%Install
# Install the kernel modules
rm -rf $RPM_BUILD_ROOT
KVER="`perl -e '$/ = ""; $_ = <>; m,VERSION\s*=\s*(\d)\s*PATCHLEVEL\s*=\s*(\d+)\s*SUBLEVEL\s*=\s*(\d+)\s*,ms; print  "$1.$2.$3$4"' $RPM_BUILD_DIR/linux/Makefile`"
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/swang/
cp kernel/ipc/*.ko kernel/iptables_fsl/*.ko $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/swang/

# Install the applications
(cd applications/conntrack; make install BIN_DIR=/usr/local/bin DESTDIR=$RPM_BUILD_ROOT/%{pfx})
(cd applications/ipdaemon;  make install BIN_DIR=/usr/local/bin DESTDIR=$RPM_BUILD_ROOT/%{pfx})
(cd tools;  make install BIN_DIR=/usr/local/bin DESTDIR=$RPM_BUILD_ROOT/%{pfx})

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

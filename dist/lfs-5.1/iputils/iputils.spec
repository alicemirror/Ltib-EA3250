%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for converting IP addresses and masks between various formats.
Name            : iputils
Version         : 0.0.4
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch0          : iputils-0.0.4-gcc-4.3.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1

%Build
make CC="${TOOLCHAIN_PREFIX}gcc"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr
for i in lib local/bin local/include
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/$i
done

make prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} LIBDIR=$RPM_BUILD_ROOT/%{pfx}/usr/lib INCDIR=$RPM_BUILD_ROOT/%{pfx}/usr/local/include/ install
install -s -m 755 iputils $RPM_BUILD_ROOT/%{pfx}/usr/local/bin/iputils
install -s -m 644 argh/libargh.so $RPM_BUILD_ROOT/%{pfx}/usr/lib/libargh.so

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

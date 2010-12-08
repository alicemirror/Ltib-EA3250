%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Simple program to read/write from/to any location in memory.
Name            : devmem2
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Applications/System
Source          : devmem2.tar.gz
Patch0		: devmem2-fixups-2.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
This is a simple program to read/write from/to any location in memory.
It can read or write a byte, halfword or word of memory at a time.
Care should be taken to properly align addresses to their appropriate
boundary when running on processors that care about such things.

WARNING: Writing or reading memory locations may corrupt your system,
so use this utility with extreme caution!

%Prep
%setup -n %{name}
%patch0 -p1

%Build
make CFLAGS="-DFORCE_STRICT_ALIGNMENT"

%Install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT/%{pfx}/sbin
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}/sbin

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

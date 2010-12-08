%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Memory Technology Device tools
Name            : mtd-utils
Version         : 20060302
Release         : 2
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch2          : mtd-utils-20060302-find_fs_entry.patch
Patch3          : mtd-utils-20060302-eraseall.patch
Patch4          : mtd-utils-20060302-eraseall_prog.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Extracted from the cvs snapshot: mtd-snapshot-20060302.tar.bz2 
at http://www.linux-mtd.infradead.org/


%Prep
%setup -n mtd
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
make -C util

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
make -C util DESTDIR=$RPM_BUILD_ROOT/%{pfx} SBINDIR=%{_prefix}/bin MANDIR=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd
install -m0644 include/mtd/*.h $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

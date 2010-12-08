%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for making and checking MS-DOS FAT filesystems on Linux.
Name            : dosfstools
Version         : 2.11
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Alan Tull
Group           : Applications/System
Source          : dosfstools-2.11.tar.gz
Patch0          : dosfstools-2.11-2.1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1

%Build
make CC="${TOOLCHAIN_PREFIX}gcc" CFLAGS="-Dllseek=lseek64 -D_LARGEFILE64_SOURCE"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/sbin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8

install -m 755 -s mkdosfs/mkdosfs $RPM_BUILD_ROOT/%{pfx}/sbin/mkdosfs
ln -sf mkdosfs $RPM_BUILD_ROOT/%{pfx}/sbin/mkfs.vfat
ln -sf mkdosfs $RPM_BUILD_ROOT/%{pfx}/sbin/mkfs.msdos

install -m 755 -s dosfsck/dosfsck $RPM_BUILD_ROOT/%{pfx}/sbin/dosfsck
ln -sf dosfsck $RPM_BUILD_ROOT/%{pfx}/sbin/fsck.msdos
ln -sf dosfsck $RPM_BUILD_ROOT/%{pfx}/sbin/fsck.vfat

install -m 644 mkdosfs/mkdosfs.8 $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8
ln -sf mkdosfs.8.gz $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8/mkfs.msdos.8.gz
ln -sf mkdosfs.8.gz $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8/mkfs.vfat.8.gz

install -m 644 dosfsck/dosfsck.8 $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8
ln -sf dosfsck.8.gz $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8/fsck.vfat.8.gz

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

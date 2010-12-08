%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A Linux filesystem designed to be simple, small, and to compress things well.
Name            : cramfs
Version         : 20081121
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This was made from the sourceforge.net CVS version as follows:

$ cvs -d:pserver:anonymous@cramfs.cvs.sourceforge.net:/cvsroot/cramfs login
$ cvs -z3 -d:pserver:anonymous@cramfs.cvs.sourceforge.net:/cvsroot/cramfs co -d cramfs-cvs -P linux

then I made a release file with:
$ cd cramfs-cvs
$ ./make_release  20081121


%Prep
%setup

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
install -m 755 mkcramfs $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/mkfs.cramfs
install -m 755 cramfsck $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/fsck.cramfs

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

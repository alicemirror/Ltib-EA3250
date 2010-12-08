%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Tools for the second extended (ext2) filesystem
Name		: genext2fs
Version		: 1.4.1
Release		: 2
License		: GPL
Vendor		: Freescale
Packager	: Stuart Hughes, Kumar Gala, Emil Medve
Group		: Applications/System
URL		: http://downloads.sourceforge.net/genext2fs/genext2fs-1.4.1.tar.gz
Source		: %{name}-%{version}.tar.gz
Patch0		: %{name}-makefile_in.patch
Patch1		: %{name}-%{version}-1.3.patch
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

genext2fs is a mean to generate an ext2 filesystem as a normal (non-root) user. It doesn't require
you to mount the image file to copy files on it. It doesn't even require you to be the superuser to
make device nodes

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
ac_scanf_can_malloc=no \
./configure --prefix=%{_prefix} --host=$CFGHOST
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

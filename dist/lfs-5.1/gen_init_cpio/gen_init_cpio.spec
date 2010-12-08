%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A utility to help make initramfs filesystems
Name            : gen_init_cpio
Version         : 2.6.25
Release         : rc7
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
URL             : http://kernel.org
Source          : %{name}-%{version}-%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Note: this is extracted from the Linux kernel

%Prep
%setup -n %{name}-%{version}-%{release}

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

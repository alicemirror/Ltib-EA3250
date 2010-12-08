%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Hello World test package
Name            : helloworld
Version         : 1.1
Release         : 2
License         : Public Domain, not copyrighted
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Test
Source          : %{name}-%{version}.tar.bz2
Patch1          : helloworld-1.1-sysroot.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
make prefix=%{_prefix}

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


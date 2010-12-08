%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : demo_launcher package
Name            : demo_launcher
Version         : 1.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Applications/Test
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT
make clean

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNOME virtual file-system libraries
Name            : gnome-vfs
Version         : 2.6.1.1
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
License         : GPL/LGPL
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --disable-openssl --disable-gtk-doc
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

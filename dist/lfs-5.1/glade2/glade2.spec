%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A GTK+ GUI builder
Name            : glade2
Version         : 2.6.5
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : glade-%{version}.tar.bz2
License         : GPL
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup -n glade-%{version}

%Build
./configure --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

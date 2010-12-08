%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : update-mime-database and <prefix>/share/mime/*
Name            : shared-mime-info
Version         : 0.14
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
License         : GPL
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup

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

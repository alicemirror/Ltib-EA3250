%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A program for synchronizing files over a network
Name            : rsync
Version         : 2.6.5
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Internet
Source          : %{name}-%{version}.tar.gz
Patch1          : rsync-2.6.5-va_copy-2.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
rsync_cv_HAVE_GETTIMEOFDAY_TZ=yes \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

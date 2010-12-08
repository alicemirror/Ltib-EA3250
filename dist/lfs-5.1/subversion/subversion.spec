%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Revision control system similar to CVS, but improved
Name            : subversion
Version         : 1.0.6
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.bz2
License         : Apache/BSD-style
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup 

%Build
LDFLAGS=-L$RPM_BUILD_ROOT/%{_prefix}/lib ./configure --prefix=%{_prefix} --cache-file=config.cache
make

%Install
rm -rf $RPM_BUILD_ROOT
# need to override locale setting on RH9
export LANG=C
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

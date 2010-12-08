%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : libiconv converts text from one encoding to another encoding.
Name            : libiconv
Version         : 1.11
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
URL             : http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.11.tar.gz
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : System performance tools for Linux
Name            : sysstat
Version         : 9.0.3
Release         : 1
License         : GPL
Vendor          : Freescale, Maxtrack
Packager        : John Rigby, Hamilton Vera, Stuart Hughes
Group           : Systems Administration
URL             : http://pagesperso-orange.fr/sebastien.godard/download.html
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}

%Build
if [ -n "$UCLIBC" ]
then
    config_opts='ac_cv_header_libintl_h=no'
fi
eval ${config_opts} \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install IGNORE_MAN_GROUP=y DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

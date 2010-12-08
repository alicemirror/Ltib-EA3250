%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}


Summary         : Lightweight http server for embedded systems
Name            : boa
Version         : 0.94.14rc21
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System/Servers
Source          : %{name}-%{version}.tar.gz
Patch1          : boa-0.94.14rc21-nommu.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This is the uclinux version extracted from uClinux-dist-test-20050906.tar.gz
at http://www.uclinux.org/pub/uClinux/dist/

%Prep
%setup
%patch1 -p1 

%Build
ac_cv_func_setvbuf_reversed=no \
CFLAGS="-DSERVER_ROOT='\"/etc\"' -g -Os" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/etc/conf
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/var/log/boa
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
install -m 755 src/boa $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/
install -m 755 src/boa_indexer $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/
install -m 644 examples/boa.conf $RPM_BUILD_ROOT/%{pfx}/%{base}/etc/conf/
ln -s conf/boa.conf $RPM_BUILD_ROOT/%{pfx}/%{base}/etc/boa.conf
ln -s boa $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/boa_d
perl -ni -e '
    m,#ServerName,  &&  do { $_ = "ServerName localhost\n" } ;
    m,^DocumentRoot, && do { $_ = "DocumentRoot /var/www/html\n" };
    m,^DirectoryMaker, && do { $_ = "DirectoryMaker %{_prefix}/sbin/boa_indexer\n" };
    m,^DefaultType, && do { $_ = "DefaultType text/html\n" };
    m,^ScriptAlias, &&  do { $_ = "ScriptAlias /cgi-bin/ /var/www/cgi-bin/\n"};
    print;
    ' $RPM_BUILD_ROOT/%{pfx}/%{base}/etc/conf/boa.conf

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

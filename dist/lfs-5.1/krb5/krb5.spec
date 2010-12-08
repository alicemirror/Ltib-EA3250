%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Development files needed to compile Kerberos 5 programs
Name            : krb5
Version         : 1.3.4
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          : %{name}-%{version}.tar.gz
Patch0          : krb5-fix-build-error.patch
URL             : http://web.mit.edu/Kerberos/
License         : MIT (freely distributable)
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1

%Build
config_opts='ac_cv_func_regcomp=yes ac_cv_file__etc_environment=yes ac_cv_file__etc_TIMEZONE=yes'

if  [ -n "$UCLIBC" ]
then
    config_opts="$config_opts ac_cv_func_res_search=yes" 
fi
cd src
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --enable-shared  --without-tcl
make

%Install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx} ADMIN_BINDIR=%{_prefix}/kerberos/sbin SERVER_BINDIR=%{_prefix}/kerberos/sbin CLIENT_BINDIR=%{_prefix}/kerberos/bin bindir=%{_prefix}/kerberos/bin
rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/man
for i in libcom_err.so libcom_err.a
do
    rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/$i
done
for i in ftp rcp rlogin rsh telnet compile_et
do
    rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/$i
done
for i in et_c.awk et_h.awk
do 
    rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/et/$i
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

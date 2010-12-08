%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Widely used Apache HTTP (web) Server
Name            : httpd
Version         : 2.0.54
Release         : 0
License         : Apache (distributable)
Vendor          : Freescale
Packager        : Jason Jin
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch0          : %{name}-%{version}-fsl.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1

%Build
if [ -n "$UCLIBC" ]
then
    AP_LIBS="-lpthread" \
    ./configure --prefix=%{_prefix}   \
    	--host=$CFGHOST --build=%{_build} \
	--enable-so \
	ac_cv_func_setpgrp_void=yes	\
	ac_cv_define_PTHREAD_PROCESS_SHARED=no	\
	ac_cv_sizeof_size_t=4	\
	ac_cv_sizeof_ssize_t=4
else
    ./configure --prefix=%{_prefix}   \
	--host=$CFGHOST --build=%{_build} \
	--enable-so \
	ac_cv_func_setpgrp_void=yes	\
	ac_cv_define_PTHREAD_PROCESS_SHARED=no	\
	ac_cv_sizeof_size_t=4	\
	ac_cv_sizeof_ssize_t=4
fi

make 

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
cd $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
rm -f lib/*.la

pattern=/usr
addprefix=$DEV_IMAGE
pattern=$(echo $pattern | sed -e 's/\//\\\//g')
addprefix=$(echo $addprefix | sed -e 's/\//\\\//g')
match="s/$pattern/$addprefix$pattern/"

rpmbuildroot_0=$(echo $RPM_BUILD_ROOT | sed -e 's/\//\\\//g')
rpmbuildroot_1=$(echo $rpmbuildroot_0 |sed -e 's/httpd/php/')
pfx_2=$(echo %{pfx} | sed -e 's/\//\\\//g')
prefix_3=$(echo %{_prefix} | sed -e 's/\//\\\//g')

sed -e $match ./build/config_vars.mk > ./build/config_vars-4ltib.mk.1
sed -e "s/$addprefix$pattern\/modules/$rpmbuildroot_1\/$pfx_2\/$prefix_3\/modules/" ./build/config_vars-4ltib.mk.1 > ./build/config_vars-4ltib.mk.2
sed -e "s/$addprefix$pattern\/conf/$rpmbuildroot_1\/$pfx_2\/$prefix_3\/conf/" ./build/config_vars-4ltib.mk.2 > ./build/config_vars-4ltib.mk.3
rm ./build/config_vars-4ltib.mk.1 ./build/config_vars-4ltib.mk.2

sed -e "s/libexecdir = \${exec_prefix}\/modules/libexecdir = \${exp_libexecdir}/" ./build/config_vars-4ltib.mk.3 > ./build/config_vars-4ltib.mk.4
sed -e "s/sysconfdir = \${prefix}\/conf/sysconfdir = \${exp_sysconfdir}/" ./build/config_vars-4ltib.mk.4 > ./build/config_vars-4ltib.mk
rm ./build/config_vars-4ltib.mk.3 ./build/config_vars-4ltib.mk.4

sed -e $match ./bin/apu-config > ./bin/apu-config-4ltib 

sed -e $match ./bin/apr-config > ./bin/apr-config-4ltib

cd ./bin
mv apr-config apr-config.bak
mv apr-config-4ltib apr-config
mv apu-config apu-config.bak
mv apu-config-4ltib apu-config

chmod 755 apu-config
chmod 755 apr-config
chmod 755 apxs

cd ../build
mv config_vars.mk config_var.mk.bak
mv config_vars-4ltib.mk config_vars.mk


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



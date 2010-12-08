%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The PHP HTML-embedded scripting language.
Name            : php
Version         : 5.0.4
Release         : 0
License         : PHP (distributable)
Vendor          : Freescale
Packager        : Jason Jin
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch0          : %{name}-%{version}-fsl.patch
Patch1          : php-5.0.4-iconv.patch
Patch2          : ppp-zend_strtod.patch
Patch3          : php-5.0.4-fix_cross_compile_detection.patch 
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n  %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
# Compile a version of php to run on the build machine
export PATH=$UNSPOOF_PATH
if [ ! -d build-php ]
then
    mkdir build-php

    # this is done so we don't need flex-2.5.4
    mkdir build-php/Zend
    cp Zend/zend_language_scanner.c build-php/Zend/zend_language_scanner.c
    cp Zend/zend_ini_scanner.c      build-php/Zend/zend_ini_scanner.c
fi
cd build-php
../configure --prefix=%{_prefix} --disable-libxml 
make sapi/cli/php
cd ..
cp build-php/sapi/cli/php ./sapi/cli/php-local

# Cross-compile php
export PATH=$SPOOF_PATH
perl -p -e '
    s,\$XML2_CONFIG --,\$XML2_CONFIG --prefix=\$DEV_IMAGE/%{_prefix} --,
           ' configure > configure-cross
if [ -n "$UCLIBC" ]
then
    EXTRA_CONFIG_OPTS="--without-iconv"
fi
if [ -z "$LTIB_NATIVE_BUILD" ]
then
    config_opts='ac_cv_prog_cc_cross=yes'
fi
eval $config_opts sh ./configure-cross \
	--prefix=${_prefix} --host=$CFGHOST --build=%{_build}  \
	--with-apxs2=$DEV_IMAGE/usr/bin/apxs \
	--with-mysql=$DEV_IMAGE/usr	\
	--with-mysqli=$DEV_IMAGE/usr/bin/mysql_config \
	--enable-soap --enable-sockets	\
	--with-zlib	\
	--with-zlib-dir=$DEV_IMAGE/usr   \
    --with-libxml \
    --with-libxml-dir=$DEV_IMAGE/usr $EXTRA_CONFIG_OPTS

# this is needed to stop libtool using libxml2.la from /usr/lib
perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool

# build cross php
# for now change optimisation to -Os as this works around a gcc4 bug (maybe)
# in freescale-coldfire-m68k-linux-gnu-4.1-14.i686.rpm
make CFLAGS_CLEAN="-g -Os"


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/modules
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/conf
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/htdocs

cp $DEV_IMAGE/usr/conf/httpd.conf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/conf
if [ ! -f ./sapi/cli/php.orig ]
then
 cp sapi/cli/php ./sapi/cli/php.orig
 cp sapi/cli/php-local ./sapi/cli/php
fi
make -j1 install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
cp sapi/cli/php.orig $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/php

cd $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/conf
rpmbuildroot_0=$(echo $RPM_BUILD_ROOT | sed -e 's/\//\\\//g')
pfx_1=$(echo %{pfx} | sed -e 's/\//\\\//g')
sed -e "s/$rpmbuildroot_0\/$pfx_1\///" ./httpd.conf > ./httpd.conf-new

awk 'BEGIN {add=0} {if ( /^DirectoryIndex/ ) print $0" index.php" ;else if (!add && /^AddType/) {print;print "AddType application/x-httpd-php .php";add=1;}else print}' httpd.conf-new > ~httpd.conf

if test -f ./~httpd.conf ; then  
 mv ~httpd.conf httpd.conf
 rm httpd.conf-new
fi

cd $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/htdocs
if [ ! -f phpinfo.php ]
then 
    cat <<EOF > phpinfo.php
<?php
phpinfo();
?>
EOF
fi


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



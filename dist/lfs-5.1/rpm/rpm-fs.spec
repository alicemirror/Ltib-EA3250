# this package is not relocatable as rpm-4.1 (redhat-8.0) is
# broken and does not take any notice of --prefix or set RPM_INSTALL_PREFIX
%define base %(echo %{_prefix} | sed -e s,/ltib/usr$,,)
%define pkg_name rpm


Summary         : The RPM package management system.
Name            : rpm-fs
Version         : 4.0.4
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{pkg_name}-%{version}.tar.gz
Patch0          : rpm_lfs.patch
Patch1          : rpm-4.0.4-python-configure.patch
Patch2          : rpm-4.0.4-sysconfig-configure.patch
Patch3          : rpm-4.0.4-no-usr-local.patch
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup  -n %{pkg_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
# this is needed for redhat-9.0 (nptl) or you get
# rpmdb: /opt/freescale/ltib/var/lib/rpm/__db.001: unable to initialize environment lock: Function not implemented
#
# This takes care of the horrible transition phase between linuxthreads
# and tls on Redhat 9 which breaks this old version of rpm (that we love).
#
set +e
HAS_TLS_LIBC="`ls /lib/tls/libc-2*so 2>/dev/null`" 
set -e
if [ -n "$HAS_TLS_LIBC" -a "`uname -m`" != "x86_64" ]
then
    #MIN_LIBC_VER="`eu-readelf -n /lib/libc-2*.so | perl -n -e 'm,ABI:\s+([\d.]+), && print $1'`"
    MIN_LIBC_VER=${MIN_LIBC_VER:-2.2.5}
    export LD_ASSUME_KERNEL=$MIN_LIBC_VER
    sed --version &>/dev/null || unset LD_ASSUME_KERNEL
fi

# For this package %{_prefix} is expected to end in /usr and be the
# actual path that we're installing into .
# Note: we do not put rpm into the normal 1 directory level above prefix
#       as we don't care about single user mode and it means we
#       only need to add one additional path to all our scripts.
#
# Note: make sure we are not going to install into the host's rpm
# Note: this package is hijacked to make the lpp directory as it is the 
#       bootstap package
#
var="`echo %{_prefix} | sed -e s,/usr$,,`/var"
etc="`echo %{_prefix} | sed -e s,/usr$,,`/etc"

# collapse multiple forward slashes
var="`echo $var | sed -e 's,/\+,/,g'`"
if [ "$var" = "/var" ]
then
    echo "You need to change your prefix to a value that won't over-write"
    echo "The installed host's rpm and rpm database."
    exit 1
fi

# take care of a Debian nuisance
for i in /usr/bin /bin
do
   if [ -x "$i/bzip2" ]
   then
       export BZIP2BIN=$i/bzip2
   fi
done

varprefix=$var \
lt_cv_prog_cc_static_works=no \
./configure --prefix=%{_prefix} --localstatedir=$var --sysconfdir=$etc \
--without-python --without-javaglue

make


%Install
export NO_BRP_STALE_LINK_ERROR=yes
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT

# make any user able to build rpms here
var="`echo %{_prefix} | sed -e s,/usr$,,`/var"
etc="`echo %{_prefix} | sed -e s,/usr$,,`/etc"
mkdir -p $RPM_BUILD_ROOT/%{base}/ltib/pkgs
chmod 777 $RPM_BUILD_ROOT/%{base}/ltib/pkgs
mkdir -p $RPM_BUILD_ROOT/$var/tmp
chmod 777 $RPM_BUILD_ROOT/$var/tmp
chmod 777 $RPM_BUILD_ROOT/%{_prefix}/src/rpm/*
chmod 777 $RPM_BUILD_ROOT/%{_prefix}/src/rpm/RPMS/*
mkdir -p $RPM_BUILD_ROOT/$etc/rpm
chmod 755 $RPM_BUILD_ROOT/$etc/rpm

# disable the perl dependency tracking, which is inappropriate for
# cross use, and in any case optimistic
chmod -x  $RPM_BUILD_ROOT/%{_prefix}/lib/rpm/perl.req

# fixup paths 
cd $RPM_BUILD_ROOT/%{_prefix}/lib/rpm
perl -pi -e 's,([ :])/usr/lib/rpm,\1%{_prefix}/lib/rpm,g' cpanflute cpanflute2 find-provides find-provides.perl find-requires find-requires.perl macros rpmpopt-4.0.4 rpmrc trpm
cd -

# Handle hosts that may conflict with targets
%ifarch ppc ppc64
echo "%""__find_requires %{_prefix}/lib/rpm/find-requires objdump" > $RPM_BUILD_ROOT/$etc/rpm/macros
%endif

%Post
# Brutally remove and re-initialise the database.  We do this as
# we're private and we have to cope with forward and backward
# compatibility issues
#
var="`echo %{_prefix} | sed -e s,/usr$,,`/var"
var="`echo $var | sed -e 's,/\+,/,g'`"
if [ "$var" = "/var" ]
then
    echo "You need to change your prefix and rebuild this rpm so that"
    echo "you won't over-write the installed host's rpm and rpm database."
    exit 1
fi
cp -a $var/lib/rpm $var/lib/rpm.bak
rm -f $var/lib/rpm/*
%{_prefix}/bin/rpm --initdb

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{base}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The RPM package management system.
Name            : rpm
Version         : 4.0.4
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
Source1         : %{name}-%{version}-macros
Patch0          : rpm_lfs.patch
Patch1          : rpm-4.0.4-python-configure.patch
Patch2          : rpm-4.0.4-no-static.patch
Patch3          : rpm-4.0.4-rpmio_h.patch
Patch4          : rpm-4.0.4-arm-gas.patch
Patch5          : rpm-4.0.4-sysconfig-configure.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : zlib

%Description
%{summary}

Modifications: 

 * Allow short circuited builds to produce binary rpms for incremental deploy

%Prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%Build
case "$LINTARCH" in
    arm*)
        mutex_type="POSIX/pthreads/library"
        ;;
    i386|i686)
        mutex_type="x86/gcc-assembly"
        ;;
    m68k)
        mutex_type="68K/gcc-assembly"
        ;;
    ppc|powerpc)
        mutex_type="PPC/gcc-assembly"
        ;;
    ppc64)
        mutex_type="POSIX/pthreads/library"
        ;;
    *)
       echo "dont know how to handle mutexes for $LINTARCH"
       exit 1
       ;;
esac

# obviously these need to be fixed for 64bit machines
ac_cv_have_working_aio=yes \
ac_cv_sizeof_char=1 \
ac_cv_sizeof_unsigned_char=1 \
ac_cv_sizeof_short=2 \
ac_cv_sizeof_unsigned_short=2 \
ac_cv_sizeof_int=4 \
ac_cv_sizeof_unsigned_int=4 \
ac_cv_sizeof_long=4 \
ac_cv_sizeof_unsigned_long=4 \
ac_cv_sizeof_long_long=8 \
ac_cv_sizeof_unsigned_long_long=8 \
ac_cv_sizeof_float=4 \
ac_cv_sizeof_double=8 \
db_cv_alignp_t="unsigned long" \
db_cv_mutex="$mutex_type" \
db_cv_fcntl_f_setfd="yes" \
db_cv_sprintf_count="yes" \
ac_cv_header_libintl_h="no" \
gt_cv_func_gnugettext1_libintl="no" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --localstatedir=/var --sysconfdir=%{_sysconfdir} --mandir=%{_mandir} --without-python --without-javaglue --disable-static

# popt ignore the --disable static for it's test programs
make test1_LDFLAGS= test2_LDFLAGS=

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la
cp %{SOURCE1} $RPM_BUILD_ROOT/%{pfx}/usr/lib/rpm/macros
perl -pi -e 's,i386,$ENV{LINTARCH},g;' $RPM_BUILD_ROOT/%{pfx}/usr/lib/rpm/macros

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



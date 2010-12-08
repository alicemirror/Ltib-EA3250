%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : gdbm
Name            : gdbm
Version         : 1.8.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Yu Liu / Alan Carvalho de Assis / Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
Patch1          : gdbm-1.8.3-ubuntu.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}
GNU dbm ('gdbm') is a library of database functions that use extensible hashing
and works similarly to the standard UNIX 'dbm' functions.

The basic use of 'gdbm' is to store key/data pairs in a data file, thus
providing a persistent version of the 'dictionary' Abstract Data Type ('hash'
to perl programmers).

This package can be found here: http://ftp.gnu.org/gnu/gdbm/

%Prep
%setup
%patch1 -p1

%Build
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`

./configure --prefix=/usr --host=$OPT_CFGHOST --build=%{_build} --mandir=%{_mandir}

echo "/* We use fcntl locking (POSIX) instead of flock (BSD) */" >> autoconf.h
echo "#undef HAVE_FLOCK" >> autoconf.h

make
make gdbm.info

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 INSTALL_ROOT=$RPM_BUILD_ROOT/%{pfx} install install-compat
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f
ln -s ndbm.h $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/gdbm-ndbm.h

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*



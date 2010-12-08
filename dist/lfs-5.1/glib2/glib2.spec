%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library of functions used by GDK, GTK+, and many applications
Name            : glib2
Version         : 2.14.3
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes/Kurt Mahan
Group           : System Environment/Libraries
Source          : glib-%{version}.tar.gz
Patch1          : glib2-2.12.11-relink.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n glib-%{version}
%patch1 -p1

%Build
# prevent configure from trying to compile and
# run test binaries for the target.
glib_cv_stack_grows=no \
glib_cv_uscore=no \
ac_cv_func_posix_getpwuid_r=yes \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A C library for parsing command line parameters.
Name            : popt
Version         : 1.7
Release         : 1
License         : X11 style
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          :  http://gd.tuwien.ac.at/utils/rpm.org/dist/rpm-4.1.x/%{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
if [ -n "$UCLIBC" ]
then
    config_opts='ac_cv_header_libintl_h=no gt_cv_func_gnugettext1_libintl=no'
fi
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
--mandir=%{_mandir} -C

# test1_LDFLAGS etc is needed for gcc-3.4.3 and later
make test1_LDFLAGS= test2_LDFLAGS= test3_LDFLAGS= LIBS="$LIBS"

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

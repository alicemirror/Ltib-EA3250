%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A collection of basic system utilities
Name            : util-linux
Version         : 2.13
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Michael Reiss/Stuart Hughes
Group           : System Environment/Base
Source          : util-linux_2.13.orig.tar.gz
Patch0          : util-linux_2.13-8.diff.gz
Patch1          : util-linux-2.13-fixups.patch
Patch2          : util-linux-2.12-fdiskbsdlabel_h_m68k.patch
Patch3          : util-linux-2.12-cf-bitops_h.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This package pulled from  http://packages.debian.org/source/lenny/util-linux

%Prep
%setup -n util-linux-ng-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
# prevent re-run of autoconf/header
touch aclocal.m4 config.h.in Makefile.in configure

if [ -n "$UCLIBC" ]
then
    config_opts='ac_cv_header_libintl_h=no gt_cv_func_gnugettext1_libintl=no'
fi
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir} --disable-use-tty-group
make 

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for ALSA (Advanced Linux Sound Architecture)
Name            : alsa-utils
Version         : 1.0.11rc2
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille/Matt Waddel
Group           : Applications/System
Source          : alsa-utils-%{version}.tar.bz2
Patch1          : alsa-utils-1.0.10-cf.patch
Patch2          : alsa-utils-1.0.11rc2-ldl.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

# 1.0.11rc2 is compatible with linux 2.6.16 kernels
#   (see linux/include/sound/version.h)

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
if [ -n "$UCLIBC" ]
then
    config_opts='gt_cv_func_gnugettext1_libintl=no'
fi
if [ "$GNUTARCH" = m68knommu ]
then
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} -C --disable-shared
else
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} -C
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

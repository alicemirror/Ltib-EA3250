%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A libraries for ALSA (Advanced Linux Sound Architecture)
Name            : alsa-lib
Version         : 1.0.18
Release         : 0
License         : LGPL
Vendor          : Freescale
Packager        : Ross Wille/Wang Huan
Group           : System Environment/Libraries
Source          : alsa-lib-%{version}.tar.bz2
Patch0          : alsa-lib-1.0.18-nommu.patch
Patch1          : alsa-lib-1.0.18-relink.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
config_args="--disable-python"
if [ "$GNUTARCH" = m68knommu ]
then
    config_args="$config_args --disable-shared" 
fi
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} $config_args
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/alsa-lib/*/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

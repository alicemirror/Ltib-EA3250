%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Netperf is used to measure the performance of of the network
Name            : netperf
Version         : 2.4.4
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Kim Phillips/Matt Waddel
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
Patch1          : netperf-2.4.4-vfork.patch
Patch2          : netperf-2.4.4-fix-cpuset.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build

# Build netserver and netperf for the host
ORIG_PATH=$PATH
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`
export PATH=$UNSPOOF_PATH
./configure --prefix=%{_prefix} --target=$CFGHOST
make
cp -a src/netperf $TOP/bin/netperf
cp -a src/netserver $TOP/bin/netserver
export PATH=$ORIG_PATH

# Build netserver and netperf for the target
make distclean
ac_cv_func_setpgrp_void=yes \
./configure --prefix=%{_prefix} --host=$OPT_CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

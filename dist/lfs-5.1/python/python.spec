%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : An interpreted object-oriented programming language.
Name            : python
Version         : 2.4.4
Release         : 1
License         : OSI Approved Python License
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
Source          : Python-%{version}.tar.bz2
Patch0          : python-2.4.4-cross-compile.diff
Patch1          : python-2.4.4-kill-dbpaths.patch
Patch2          : python-2.4.4-cross-compile-missing-modules.diff
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0

%Build
#
# Note: This cross compile method is adapted from: 
#       http://www.ailis.de/~k/docs/crosscompiling/python.php
#
# build a version for the machine we are building on, before we
# build for the target
#

ORIG_PATH=$PATH
export PATH=$UNSPOOF_PATH
./configure
make python Parser/pgen
mv python hostpython
mv Parser/pgen Parser/hostpgen

make distclean

export PATH=$ORIG_PATH

LDFLAGS="-L$DEV_IMAGE/usr/lib" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --enable-shared --without-libdb --without-ssl

make HOSTPYTHON=./hostpython  HOSTPGEN=./Parser/hostpgen CROSS_COMPILE=yes

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} HOSTPYTHON=./hostpython \
     CROSS_COMPILE=yes install  

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

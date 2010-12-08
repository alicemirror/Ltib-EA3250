%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Clutter is an open-source library for creating animated GUIs.
Name            : clutter
Version         : 0.6.2
Release         : 0
License         : LGPL
Vendor          : Freescale
Packager        : Ross Wille, Fabio Estevam, John Faith
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
export TSLIB_CFLAGS=-I$DEV_IMAGE/usr/include
export TSLIB_LIBS="-L$DEV_IMAGE/usr/lib -lts"
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
 --with-flavour=eglnative --disable-gtk-doc
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

# Tests install workaround
export TESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/clutter
mkdir -p $TESTDIR
cp -a tests/.libs/* $TESTDIR
cp tests/redhand.png tests/test-script.json $TESTDIR


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

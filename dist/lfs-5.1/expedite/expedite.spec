%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : This is meant to be a detailed and comprehensive benchmark suite for Evas.
Name            : expedite
Version         : 0.6.0
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : Applications
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : evas

%Description
This is meant to be a detailed and comprehensive benchmark suite for Evas.

%Prep
%setup

%Build

if rpm --dbpath %{_dbpath} -q xorg-server &>/dev/null; then PKG_XORG="yes" ; fi
if rpm --dbpath %{_dbpath} -q DirectFB &>/dev/null; then PKG_DIRECTFB="yes" ; fi

if [ -n "$PKG_DIRECTFB" ]
then 
	XTRA_OPTS="--enable-directfb"
else
	XTRA_OPTS="--disable-directfb"
fi

if [ -n "$PKG_XORG" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-software-x11 --enable-xrender-x11"
else
	XTRA_OPTS="$XTRA_OPTS --disable-software-x11 --disable-xrender-x11"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} $XTRA_OPTS 
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Ecore is an event/X abstraction layer
Name            : ecore
Version         : 0.9.9.050
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Ecore is the event/X abstraction layer that makes doing selections,
Xdnd, general X stuff, event loops, timeouts and idle handlers fast,
optimized, and convenient. It's a separate library so anyone can make
use of the work put into Ecore to make this job easy for applications.

%Prep
%setup

%Build
XTRA_OPTS="--enable-ecore-fb"

if rpm --dbpath %{_dbpath} -q xorg-server &>/dev/null; then PKG_XORG="yes" ; fi
if rpm --dbpath %{_dbpath} -q evas &>/dev/null; then PKG_EVAS="yes" ; fi
if rpm --dbpath %{_dbpath} -q DirectFB &>/dev/null; then PKG_DIRECTFB="yes" ; fi

if [ -n "$PKG_XORG" ]
then
	XTRA_OPTS="$XTRA_OPTS --enable-ecore-x"
else
	XTRA_OPTS="$XTRA_OPTS --disable-ecore-x"
fi

if [ -n "$PKG_DIRECTFB" ]
then
	XTRA_OPTS="$XTRA_OPTS --enable-ecore-directfb"
	if [ -n "$PKG_EVAS" ]
	then
		XTRA_OPTS="$XTRA_OPTS --enable-ecore-evas-dfb"
	else
		XTRA_OPTS="$XTRA_OPTS --disable-ecore-evas-dfb"
	fi	
else
	XTRA_OPTS="$XTRA_OPTS --disable-ecore-directfb"
fi


./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} $XTRA_OPTS 
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f 

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


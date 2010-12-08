%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Media integration library for Enlightenment
Name            : emotion
Version         : 0.1.0.042
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : evas edje ecore

%Description
%{summary}

%Prep
%setup

%Build
XTRA_OPTS="--disable-xine"

if rpm --dbpath %{_dbpath} -q gstreamer-core &>/dev/null; then PKG_GSTREAMER_CORE="yes" ; fi

if [ -n "$PKG_GSTREAMER_CORE" ]
then
    XTRA_OPTS="$XTRA_OPTS --enable-gstreamer"
else
    XTRA_OPTS="$XTRA_OPTS --disable-gstreamer"
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


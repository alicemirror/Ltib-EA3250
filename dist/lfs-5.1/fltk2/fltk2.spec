%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : FLTK2 Graphic library
Name            : fltk2
Version         : 2.0.x 
Release         : r6793
License         : LGPL with exceptions
Vendor          : Maxtrack
Packager        : Alan Carvalho, Hamilton Vera
Group           : Development/Libraries
URL             : http://www.fltk.org/
Source          : fltk-%{version}-%{release}.tar.bz2
Patch3          : fltk-2.0.x-fixfontcrash.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -q -n fltk-%{version}-%{release}
%patch3 -p1

%Build
if [ -z "$PKG_FLTK2_WANT_FLUID" ]
then
    perl -pi.orig -e 's,^(DIRS.*)fluid ,$1,' Makefile
fi
if [ -z "$PKG_FLTK2_WANT_GLUTDEMOS" ]
then
    perl -pi.orig -e 's,(all:.*)\$\(DEMOS\),$1,' glut/Makefile
fi
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --disable-xft --disable-gl --with-x --disable-xinerama 
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

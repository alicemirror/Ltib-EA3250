%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : DirectFB is a graphics library for embedded systems
Name            : DirectFB
Version         : 1.1.0
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : WMSG
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
Patch1          : DirectFB-1.1.0-ppcasm.patch
Patch4          : DirectFB-0.9.24-relink.patch
Patch5          : DirectFB-1.1.0-linux-config-h.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch4 -p1
%patch5 -p1

%Build
KHDR_DIR=$DEV_IMAGE/usr/src/linux/include
if [ ! -f $KHDR_DIR/linux/autoconf.h ]
then
    cat <<TXT

No file: $KHDR_DIR/linux/autoconf.h

You need to build the kernel and have 'Include kernel headers' set
to build this package

TXT
    exit 1
fi
export FREETYPE_CONFIG=${DEV_IMAGE}/usr/bin/freetype-config
export FREETYPE_CFLAGS="`${FREETYPE_CONFIG} --prefix=${DEV_IMAGE}/%{_prefix} --cflags`"
export FREETYPE_LIBS="`${FREETYPE_CONFIG} --prefix=${DEV_IMAGE}/%{_prefix} --libs`"

if [ -n "$PKG_DIRECTFB_WANT_TS" ]
then
    TSOPTS="--with-inputdrivers=tslib,keyboard,linuxinput"
fi
./configure --enable-shared --host=$CFGHOST --build=%{_build} \
            --prefix=%{_prefix} --with-gfxdrivers=none \
            --disable-x11 --enable-fbdev --enable-video4linux2 --disable-sdl \
            --enable-zlib $TSOPTS

perl -p -i -e 's,^#define\s+HAVE_ASM_PAGE_H\s+1,/\* #define HAVE_ASM_PAGE_H 1 \*/,' config.h
make KHDR=$KHDR_DIR

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name \*.la | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

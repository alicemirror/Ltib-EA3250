%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Evas is a clean display canvas API
Name            : evas
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
#BuildRequires   : freetype

%Description
Evas is a clean display canvas API for several target display systems
that can draw anti-aliased text, smooth super and sub-sampled scaled
images, alpha-blend objects much and more.

%Prep
%setup

%Build
XTRA_OPTS="--enable-fb --disable-cpu-mmx --disable-cpu-sse --disable-cpu-altivec --disable-image-loader-gif --disable-image-loader-xpm --disable-image-loader-svg --enable-no-dither-mask"

if rpm --dbpath %{_dbpath} -q DirectFB &>/dev/null; then PKG_DIRECTFB="yes" ; fi
if rpm --dbpath %{_dbpath} -q fontconfig &>/dev/null; then PKG_FONTCONFIG="yes" ; fi
if rpm --dbpath %{_dbpath} -q xorg-server &>/dev/null; then PKG_XORG="yes" ; fi
if rpm --dbpath %{_dbpath} -q libtiff &>/dev/null; then PKG_LIBTIFF="yes" ; fi
if rpm --dbpath %{_dbpath} -q libpng &>/dev/null; then PKG_LIBPNG="yes" ; fi
if rpm --dbpath %{_dbpath} -q eet &>/dev/null; then PKG_EET="yes" ; fi


if [ -n "$PKG_DIRECTFB" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-directfb"
else
	XTRA_OPTS="$XTRA_OPTS --disable-directfb"
fi

if [ -n "$PKG_FONTCONFIG" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-fontconfig"
else
	XTRA_OPTS="$XTRA_OPTS --disable-fontconfig"
fi

if [ -n "$PKG_XORG" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-software-x11 --enable-xrender-x11 --enable-software-16-x11"
else
	XTRA_OPTS="$XTRA_OPTS --disable-software-x11 --disable-xrender-x11 --disable-software-16-x11"
fi

if [ -n "$PKG_LIBTIFF" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-image-loader-tiff"
else
	XTRA_OPTS="$XTRA_OPTS --disable-image-loader-tiff"
fi

if [ -n "$PKG_LIBPNG" ]
then 
	XTRA_OPTS="$XTRA_OPTS --enable-image-loader-pmaps"
else
	XTRA_OPTS="$XTRA_OPTS --disable-image-loader-pmaps"
fi

if [ -n "$PKG_EET" ]
then
	XTRA_OPTS="$XTRA_OPTS --enable-image-loader-eet --enable-font-loader-eet"
else
	XTRA_OPTS="$XTRA_OPTS --disable-image-loader-eet --disable-font-loader-eet"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} $XTRA_OPTS CFLAGS="-O0 -g"
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


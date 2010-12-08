%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 Protocol headers
Name            : xorg-x11-proto-devel
Version         : 7.3
Release         : 12
License         : MIT
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : Development/System
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/proto/bigreqsproto-1.0.2.tar.bz2
Source1         : ftp://ftp.x.org/pub/individual/proto/compositeproto-0.4.tar.bz2
Source2         : ftp://ftp.x.org/pub/individual/proto/damageproto-1.1.0.tar.bz2
Source3         : ftp://ftp.x.org/pub/individual/proto/dmxproto-2.2.2.tar.bz2
Source4         : ftp://ftp.x.org/pub/individual/proto/evieext-1.0.2.tar.bz2
Source5         : ftp://ftp.x.org/pub/individual/proto/fixesproto-4.0.tar.bz2
Source6         : ftp://ftp.x.org/pub/individual/proto/fontcacheproto-0.1.2.tar.bz2
Source7         : ftp://ftp.x.org/pub/individual/proto/fontsproto-2.0.2.tar.bz2
Source8         : ftp://ftp.x.org/pub/individual/proto/glproto-1.4.9.tar.bz2
Source9         : ftp://ftp.x.org/pub/individual/proto/inputproto-1.4.3.tar.bz2
Source10        : ftp://ftp.x.org/pub/individual/proto/kbproto-1.0.3.tar.bz2
Source11        : ftp://ftp.x.org/pub/individual/proto/randrproto-1.2.1.tar.bz2
Source12        : ftp://ftp.x.org/pub/individual/proto/recordproto-1.13.2.tar.bz2
Source13        : ftp://ftp.x.org/pub/individual/proto/renderproto-0.9.3.tar.bz2
Source14        : ftp://ftp.x.org/pub/individual/proto/resourceproto-1.0.2.tar.bz2
Source15        : ftp://ftp.x.org/pub/individual/proto/scrnsaverproto-1.1.0.tar.bz2
Source16        : ftp://ftp.x.org/pub/individual/proto/trapproto-3.4.3.tar.bz2
Source17        : ftp://ftp.x.org/pub/individual/proto/videoproto-2.2.2.tar.bz2
Source18        : ftp://ftp.x.org/pub/individual/proto/xcmiscproto-1.1.2.tar.bz2
Source19        : ftp://ftp.x.org/pub/individual/proto/xextproto-7.0.2.tar.bz2
Source20        : ftp://ftp.x.org/pub/individual/proto/xf86bigfontproto-1.1.2.tar.bz2
Source21        : ftp://ftp.x.org/pub/individual/proto/xf86dgaproto-2.0.3.tar.bz2
Source22        : ftp://ftp.x.org/pub/individual/proto/xf86driproto-2.0.4.tar.bz2
Source23        : ftp://ftp.x.org/pub/individual/proto/xf86miscproto-0.9.2.tar.bz2
Source24        : ftp://ftp.x.org/pub/individual/proto/xf86rushproto-1.1.2.tar.bz2
Source25        : ftp://ftp.x.org/pub/individual/proto/xf86vidmodeproto-2.2.2.tar.bz2
Source26        : ftp://ftp.x.org/pub/individual/proto/xineramaproto-1.1.2.tar.bz2
Source27        : ftp://ftp.x.org/pub/individual/proto/xproto-7.0.12.tar.bz2
Source28        : ftp://ftp.x.org/pub/individual/proto/xproxymanagementprotocol-1.0.2.tar.bz2
Source29        : http://xorg.freedesktop.org/archive/individual/proto/dri2proto-1.1.tar.bz2

Patch0          : inputproto-1.4.3-card32-sucks.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xorg-x11-proto-devel-7.3-12.fc9.src.rpm

%Prep

%setup -q -c xorg-x11-proto-devel-7.3 -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a26 -a27 -a28 -a29
%patch0 -p0 -b .card32


%Build
# Proceed through each proto package directory, building them all
for dir in $(ls -1) ; do
	pushd $dir
	./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} 
	make
	mv COPYING COPYING-${dir%%-*}
	popd
done


%Install
rm -rf $RPM_BUILD_ROOT
for dir in $(ls -1) ; do
	pushd $dir
	make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
	install -m 444 COPYING-${dir%%-*} $OLDPWD
	popd
done
#for i in composite damage randr render ; do
#    mv $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/doc/${i}proto/${i}proto.txt .
#done
# this header is supposed to come from Mesa, not driproto
rm -f $RPM_BUILD_ROOT/%{_includedir}/GL/internal/dri_interface.h

# libXext still needs XLbx.h and lbxstr.h to build.  The rest are junk.
rm -f $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbxbuf.h \
      $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbxbufstr.h \
      $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbxdeltastr.h \
      $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbximage.h \
      $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbxopts.h \
      $RPM_BUILD_ROOT%{_includedir}/X11/extensions/lbxzlib.h

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

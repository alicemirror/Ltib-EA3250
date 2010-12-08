%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 X server utilities
Name            : xorg-x11-server-utils
Version         : 7.4
Release         : 7
License         : MIT
Vendor          : LTIB addsrpms
Packager        : LTIB addsrpms
Group           : User Interface/X
URL             : http://www.x.org
Source0:  http://www.x.org/pub/individual/app/iceauth-1.0.2.tar.bz2
Source2:  http://www.x.org/pub/individual/app/rgb-1.0.1.tar.bz2
Source3:  http://www.x.org/pub/individual/app/sessreg-1.0.4.tar.bz2
Source4:  http://www.x.org/pub/individual/app/xcmsdb-1.0.1.tar.bz2
Source5:  http://www.x.org/pub/individual/app/xgamma-1.0.2.tar.bz2
Source6:  http://www.x.org/pub/individual/app/xhost-1.0.2.tar.bz2
Source7:  http://www.x.org/pub/individual/app/xmodmap-1.0.3.tar.bz2
Source8:  http://www.x.org/pub/individual/app/xrandr-1.2.99.4.tar.bz2
Source9:  http://www.x.org/pub/individual/app/xrdb-1.0.5.tar.bz2
Source10: http://www.x.org/pub/individual/app/xrefresh-1.0.2.tar.bz2
Source11: http://www.x.org/pub/individual/app/xset-1.0.4.tar.bz2
Source12: http://www.x.org/pub/individual/app/xsetmode-1.0.0.tar.bz2
Source13: http://www.x.org/pub/individual/app/xsetpointer-1.0.1.tar.bz2
Source14: http://www.x.org/pub/individual/app/xsetroot-1.0.2.tar.bz2
Source15: http://www.x.org/pub/individual/app/xstdcmap-1.0.1.tar.bz2
Source16: http://www.x.org/pub/individual/app/xvidtune-1.0.1.tar.bz2
Patch1100: rgb-1.0.0-datadir-rgbpath-fix.patch
Patch1200: xset-1.0.2-spurious-xprint.patch
Patch1700: xvidtune-1.0.1-buffer-stomp.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xorg-x11-server-utils-7.4-7.fc11.src.rpm

%Prep

%setup -q -c %{name}-%{version} -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16

%patch1100 -p0 -b .datadir-rgbpath-fix
%patch1200 -p0 -b .xprint
#%patch1700 -p0 -b .datadir-app-defaults-fix
%patch1700 -p1 -b .buffer-stomp


%Build
# Remove the components that don't build due to unmet dependancies
# I think these are on the build machine, but I'm not sure.
# xgamma needs x11 (ok) xxf86vm (bad for non x86)
# xrandr needs xrandr xrender (I think hosts deps, so I'll exclude
# xsetmode needs xi
# xsetpointer needs xi
# xsetroot needs xbitmaps
# xstdcmap needs xxf86vm
# xvidtune needs xxf86vm
rm -rf xgamma-1.0.2 xrandr-1.2.99.4 xsetmode-1.0.0 xsetpointer-1.0.1 xsetroot-1.0.2 xstdcmap-1.0.1 xvidtune-1.0.1

# Build all apps
{
   for app in * ; do
      pushd $app
      ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
      make
      popd
   done
}


%Install
rm -rf $RPM_BUILD_ROOT/%{pfx}/
# Install all apps
{
   for app in * ; do
      pushd $app
      case $app in
         *)
            make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}/
            ;;
      esac
      popd
   done
}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

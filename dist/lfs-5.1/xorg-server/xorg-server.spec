%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org server
Name            : xorg-server
Version         : 1.4.2
Release         : 1
License         : X11
Vendor          : X.Org Foundation
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.x.org/
Source          : %{name}-%{version}.tar.bz2
Patch1          : xorg-server-1.4-kmode.patch
Patch2          : xorg-server-1.4.2-configure.patch
Patch3          : xorg-server-1.4.2-u16.patch
Patch4          : xorg-server-1.4.2-mouse-protocol.patch 
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
The official package for X.Org server, being compiled with kdrive.

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
if rpm --dbpath %{_dbpath} -q tslib &>/dev/null
then
    extra_opts='--enable-tslib --disable-xkb --disable-dga'
else
    extra_opts='--enable-xkb --disable-ipv6'
fi

# By default we'll use the original options that build kdrive 
# and override the ones we need for a full Xorg
if [ -n "$PKG_XORG_SERVER_WANT_XORG" ]
then
    extra_opts="$extra_opts --enable-xorg --enable-dga"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --enable-composite  --enable-kdrive --disable-dri --disable-xinerama --disable-xf86misc --disable-xf86vidmode --disable-xorg --disable-xorgcfg --disable-xnest --disable-xvfb --disable-xevie --disable-xprint --disable-xtrap --enable-xfbdev  --disable-dmx --enable-builtin-fonts --disable-dbus $extra_opts

perl -000 -pi.bak -e 's,-lts,, if m,^Xfbdev_DEPENDENCIES|Xephyr_DEPENDENCIES,' \
                              hw/kdrive/fbdev/Makefile hw/kdrive/ephyr/Makefile

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


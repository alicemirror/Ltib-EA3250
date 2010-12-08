%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 xkb utilities
Name            : xorg-x11-xkb-utils
Version         : 7.2
Release         : 8
License         : MIT
Vendor          : LTIB addsrpms
Packager        : LTIB addsrpms
Group           : User Interface/X
URL             : http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/app/xkbutils-1.0.1.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/app/xkbcomp-1.0.5.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/app/xkbevd-1.0.2.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/app/xkbprint-1.0.1.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/app/setxkbmap-1.0.4.tar.bz2
Patch1: xkbcomp-1.0.5-dont-overwrite.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xorg-x11-xkb-utils-7.2-8.fc11.src.rpm

%Prep

%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
%patch1 -p0 -b .dont-overwrite


%Build
export CFLAGS="-DHAVE_STRCASECMP"
for pkg in xkbutils setxkbmap xkbcomp xkbevd xkbprint ; do
    pushd $pkg-*
    ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
    make
    popd
done


%Install
rm -rf $RPM_BUILD_ROOT
for pkg in xkbutils setxkbmap xkbcomp xkbevd xkbprint ; do
    pushd $pkg-*
    make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
    popd
done


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

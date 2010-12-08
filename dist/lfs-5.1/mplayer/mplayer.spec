%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : mplayer
Name            : mplayer
Version         : 1.0~rc2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Wang Huan
Group           : Applications/System
Source          : %{name}_%{version}.orig.tar.gz
Patch0          : mplayer_1.0~rc2-17+lenny3.diff
Patch1          : mplayer-1.0~rc2-m68knommu-1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://packages.debian.org/en/lenny/mplayer

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%Build
# Currently only audio on m68knommu platforms is configed.
./configure --cc=m68k-uclinux-gcc \
	--host-cc="$BUILDCC" \
	--enable-cross-compile \
	--target=m68k-uclinux \
	--disable-dvdread \
	--enable-fbdev \
	--disable-mencoder \
	--enable-libavcodec_a \
	--enable-libavutil_a \
	--enable-libavformat_a \
	--enable-libpostproc_a \
	--enable-liba52 \
	--disable-mp3lib \
	--enable-static \
	--disable-gui \
	--disable-ivtv \
	--disable-live \
	--disable-dvdnav \
	--disable-dvdread \
	--disable-dvdread-internal \
	--disable-libdvdcss-internal 
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp mplayer $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

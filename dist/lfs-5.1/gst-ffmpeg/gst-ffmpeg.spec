%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : GStreamer plugin for FFmpeg codecs
Name            : gst-ffmpeg
Version         : 0.10.3
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : John Faith
Group           : Applications/System
Source          : %{name}-%{version}.tar.bz2
Patch1          : gst-ffmpeg-0.10.3-relink.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://gstreamer.freedesktop.org/src/gst-ffmpeg

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
ac_cv_func_register_printf_function=no \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --without-check --disable-altivec
DEBUG_CFLAGS="-g" make
#make


%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


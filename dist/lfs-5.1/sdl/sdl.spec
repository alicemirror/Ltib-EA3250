%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A cross-platform multimedia library.
Name            : SDL
Version         : 1.2.13
Release         : 1
Source          : http://www.libsdl.org/release/%{name}-%{version}.tar.gz
URL             : http://www.libsdl.org/
License         : LGPL
Group           : System Environment/Libraries
BuildRoot                  :  %{_tmppath}/%{name}
Prefix          : %{_prefix}


%Description
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

%Prep
%setup

%Build
./configure  --host=$CFGHOST --build=%{_build} --enable-cross-compile --prefix=%{_prefix} --disable-video-aalib --disable-video-directfb --disable-video-ggi --disable-video-svga --mandir=%{_mandir}  --disable-esd

perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool

make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


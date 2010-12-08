%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : FFmpeg video and sound codecs and utilities.
Name            : ffmpeg
Version         : 20080916
Release         : 1
License         : LGPL
Vendor          : Freescale Semiconductor
Packager        : John Faith
Group           : Applications
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://ffmpeg.mplayerhq.hu/download.html

%Description
%{summary}

%Prep
%setup -n ffmpeg-export-2008-09-16

%Build
./configure --arch=$LINTARCH --disable-altivec --disable-mmx --disable-mmx2 --enable-cross-compile --prefix=%{_prefix} --mandir=%{_mandir} --extra-cflags=-I../linux/include
make

%Install
rm -rf $RPM_BUILD_ROOT
make install INSTALL=cp DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


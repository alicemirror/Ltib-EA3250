%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Terminal emulator for the X Window System
Name            : xterm
Version         : 234
Release         : 1
License         : MIT
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : User Interface/X
URL             : http://dickey.his.com/xterm
Source0         : ftp://invisible-island.net/xterm/xterm-234.tgz
Source1         : ftp://invisible-island.net/xterm/16colors.txt
Source2         : xterm.desktop
Patch1          : xterm-223-resources.patch
Patch2          : xterm-222-can-2003-0063.patch
Patch3          : xterm-226-man-page_paths.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xterm-234-1.fc9.src.rpm

%Prep
%setup -q


%Build
./configure \
    --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	--enable-256-color \
	--enable-warnings \
	--with-tty-group=tty \
	--disable-full-tgetent
make

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

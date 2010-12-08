%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Xorg X11 keyboard input driver
Name            : xorg-x11-drv-keyboard
Version         : 1.3.0
Release         : 3
License         : MIT
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : User Interface/X Hardware Support
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/driver/xf86-input-keyboard-1.3.0.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xorg-x11-drv-keyboard-1.3.0-3.fc9.src.rpm

%Prep

%setup -q -n xf86-input-keyboard-1.3.0


%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
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

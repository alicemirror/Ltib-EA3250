%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 twm window manager
Name            : xorg-x11-twm
Version         : 1.0.3
Release         : 2
License         : MIT/X11
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : User Interface/X
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/app/twm-1.0.3.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms xorg-x11-twm-1.0.3-2.fc9.src.rpm

%Prep

%setup -q -n twm-1.0.3


%Build
# FIXME: Work around pointer aliasing warnings from compiler for now
export CFLAGS="-fno-strict-aliasing"
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make


%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

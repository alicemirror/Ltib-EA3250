%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : GtkWebcam - A simple webcam viewer
Name            : gtkwebcam
Version         : 1.0.0
Release         : 0
License         : GPL
Vendor          : Maxtrack Industrial
Packager        : Alan Carvalho de Assis <alan@maxtrack.com.br>, Hamilton Vera <hvera@maxtrack.com.br>, Rogerio Souza <rogerio@maxtrack.com.br>
Group           : Applications/System
Source          : gtkwebcam-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This application is used to test external webcam which supports RGB24 format.
I tested it using a Logitech Quickcam for Notebooks Pro (046d:08b1).

%Prep
%setup

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp gtkwebcam $RPM_BUILD_ROOT/%{pfx}/usr/bin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/share/pixmaps/gtkwebcam
cp retrovisor.png $RPM_BUILD_ROOT/%{pfx}/usr/share/pixmaps/gtkwebcam

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

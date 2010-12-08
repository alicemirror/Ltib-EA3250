%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Nano-X window display program and samples
Name            : microwindows
Version         : 0.90
Release         : 1
License         : MPL/GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Applications/System
Source          : microwindows-0.90.tar.gz
Patch1		: microwindows-0.90-coldfire.patch
Patch2		: microwindows-0.90-scripts.patch
Patch3          : microwindows-0.90-uclinux.patch
Patch4          : microwindows-0.90-page-h.patch
Patch5          : microwindows-0.90-m5329.patch
Patch6          : microwindows-0.90-colormap.patch
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
Microwindows (also known as nano-x) is a very small frame buffer
based X server. Its aim is to bring the features of modern windowing
environments to smaller devices and platforms. Also included are
several utility and demo programs.  This one is modified to work
on uClinux/touchscreen devices.

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%Build
cd src
make -j1 HOSTCC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/nanox
cd src
cp -a bin/ $RPM_BUILD_ROOT/%{pfx}/usr/nanox
cp -a *.sh $RPM_BUILD_ROOT/%{pfx}/usr/nanox
# Remove build files and non-functioning demos.
for i in convbmp makebmp convbdf convpbm ftdemo getselection logfont move pcfdemo setselection snap_ppm t1demo tuxchess vnc 
do
rm -f $RPM_BUILD_ROOT/%{pfx}/usr/nanox/bin/$i
done
for i in chess.sh demo.sh font*.sh grabdemo.sh mouse.sh vnc.sh indent.sh
do
rm -f $RPM_BUILD_ROOT/%{pfx}/usr/nanox/$i
done
rm -f $RPM_BUILD_ROOT/%{pfx}/usr/nanox/bin/*.gdb

# install include files and libraries for links.
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr
cp -a include/ $RPM_BUILD_ROOT/%{pfx}/usr
cp -a lib/ $RPM_BUILD_ROOT/%{pfx}/usr

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

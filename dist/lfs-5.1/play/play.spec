%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : play - A simple wav player and audio tone tester.
Name            : play
Version         : 1.0
Release         : 0
License         : Distributable
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Applications/System
Source          : play-%{version}-%{release}.tar.gz
Patch1          : play-math-1.0.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This package comes from the uClinux.org CVS repository:
cvs.uclinux.org:/var/cvs/uClinux-dist/user/play

%Prep
%setup -n play
%patch1 -p1

%Build
make LIBM=-lm 

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/bin
cp play tone $RPM_BUILD_ROOT/%{pfx}/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Performance Monitor Register Access
Name            : pmra
Version         : 1.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Michael Barkowski
Group           : Modules
Source          : %{name}-%{version}.tar.bz2
Patch1          : pmra-1.3-1135028143.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch1 -p1

%Build
make ARCH=${LINTARCH} LINUXSRC=../linux-2.6.10 PLATFORM=${PLATFORM}

%Install
rm -rf $RPM_BUILD_ROOT
make PLATFORM=${PLATFORM} LINUXSRC=../linux-2.6.10 INSTDIR=$RPM_BUILD_ROOT/%{pfx}/opt/pmra install


%Clean
make ARCH=${LINTARCH} PLATFORM=${PLATFORM} LINUXSRC=../linux-2.6.10 clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

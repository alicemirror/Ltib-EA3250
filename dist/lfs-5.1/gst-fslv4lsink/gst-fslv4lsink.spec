%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : GStreamer Freescale V4LSINK Plugin
Name            : gst-fslv4lsink
Version         : 0.10.1
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Kurt Mahan
Group           : Applications/System
Source          : gst-fslv4lsink-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n gst-fslv4lsink-%{version}

%Build
export PKG_CONFIG="`which pkg-config` --static "
./configure --prefix=%{_prefix} --host=$CFGHOST \
	    --build=%{_build}
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

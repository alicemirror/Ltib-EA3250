%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Set of plugins for Gstreamer used Audio/Video conferencing
Name            : gst-plugins-farsight
Version         : 0.12.5
Release         : 1
License         : LGPL
Packager        : Fadi Souilem/Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST \
        --disable-jingle-p2p \
        --with-plugins=rtpmux,rtpdemux,rtpssrcdemux,rtppayloads

make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


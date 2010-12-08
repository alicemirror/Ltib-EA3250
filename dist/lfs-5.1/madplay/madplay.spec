%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : MAD is a high-quality MPEG audio decoder.
Name            : madplay
Version         : 0.15.2b
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Applications/System
Source          : madplay-0.15.2b.tar.gz
Patch0          : madplay-0.15.2b-libz.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=${_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Red Hat Liberation fonts
Name            : liberation-fonts
Version         : 20070509
Release         : 1
License         : GPL+exception
Vendor          : Freescale
Packager        : John Faith
Group           : System Environment/Base
Source          : %{name}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : https://www.redhat.com/promo/fonts/

%Description
%{summary}

%Prep
%setup -n %{name}

%Build
# NOP

%Install
fontdir=$RPM_BUILD_ROOT/%{pfx}/usr/share/fonts/liberation-fonts
mkdir -p $fontdir
cp *ttf $fontdir

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : plugin for the GNU Name Service Switch providing host name resolution via Multicast DNS
Name            : nss-mdns
Version         : 0.8
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Alan Tull
Group           : Networking
Source          : nss-mdns-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
export ac_cv_func_malloc_0_nonnull=yes
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*



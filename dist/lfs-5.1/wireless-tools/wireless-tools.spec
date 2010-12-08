%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Wireless Ethernet configuration tools
Name            : wireless-tools
Version         : 29
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : wireless_tools.%{version}.tar.gz
Patch1          : wireless-tools-29-tc-segv.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n wireless_tools.%{version}
%patch1 -p1

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%{pfx} INSTALL_INC=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/ INSTALL_MAN=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Basic networking tools
Name            : net-tools
Version         : 1.60
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : net-tools-1.60.tar.bz2
Patch0          : net-tools-1.60-miitool-gcc33-1.patch
Patch2          : net-tools-1.60-2.patch
Patch3          : net-tools-1.60-gcc34.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch2 -p1
%patch3

%Build
yes "" | make config
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 BASEDIR=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



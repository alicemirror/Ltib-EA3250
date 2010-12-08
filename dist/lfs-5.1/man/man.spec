%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : man - format and display the on-line manual pages
Name            : man
Version         : 1.5m2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.bz2
Patch0          : %{name}-%{version}-manpath.patch
Patch1          : %{name}-%{version}-pager.patch
Patch2          : %{name}-%{version}-80cols.patch
Patch3          : %{name}-%{version}-cross-compile.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
./configure -default -confdir=/etc
make -j1 CC_FOR_BUILD="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install PREFIX=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



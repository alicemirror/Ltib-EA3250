%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : procinfo - display system status gathered from /proc
Name            : procinfo
Version         : 18
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : procinfo-18.tar.gz
Patch1          : procinfo-18-mandir.patch
Patch2          : procinfo-18-siglist.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make -j1 LDLIBS=-lncurses

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



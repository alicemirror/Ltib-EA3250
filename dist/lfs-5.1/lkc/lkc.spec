%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Linux kernel configuration language parser
Name            : lkc
Version         : 1.4
Release         : 10
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
Patch0          : lkc-1.4-lxdialog.patch 
Patch1          : lkc-1.4-1.patch
Patch2          : lkc-1.4-ncurses.patch
Patch3          : lkc-1.4-help.patch
Patch4          : lkc-1.4-defaults-4.patch
Patch5          : lkc-1.4-search-5.patch
Patch6          : lkc-1.4-datestamp.patch
Patch7          : lkc-1.4-dashsource.patch
Patch8          : lkc-1.4-config_title-1.patch
Patch9          : lkc-1.4-config_filename-1.patch
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
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%Build
make -j1 conf mconf

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp -a conf mconf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



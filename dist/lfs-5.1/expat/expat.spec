%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : XML 1.0 parser
Name            : expat
Version         : 1.95.8
Release         : 1
License         : MIT/X Consortium License
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Publishing/XML
Source0         : %{name}-%{version}.tar.gz
Patch0          : %{name}-DESTDIR-%{version}.patch 
Patch1          : %{name}-ac_fixes.patch
Patch2          : expat-1.95.8-man1dir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx} install
rm $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


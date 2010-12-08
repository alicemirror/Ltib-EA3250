%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : tmake utility for building qtembedded and qtopia
Name            : tmake
Version         : 1.11
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : John Rigby
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Utility for building qtembedded and qtopia

%Prep
%setup 

%Build
# nothing to build, its a perl script
# just copy the script and the supporting files
cp -f bin/tmake $TOP/bin
rm -rf $TOP/bin/lib
cp -a lib $TOP/bin/lib

%Install
# this is a build machine thing only, nothing to get installed on 
# the target
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/tmp
touch $RPM_BUILD_ROOT/%{pfx}/tmp/.%{name}.dummy

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

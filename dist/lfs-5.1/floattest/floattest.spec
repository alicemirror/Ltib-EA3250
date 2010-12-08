%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Floating point test package
Name            : floattest
Version         : 1.0
Release         : 1
License         : Public Domain, not copyrighted
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : Applications/Test
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
gcc -o floattest floattest.c
gcc -o floattest1 floattest1.c
gcc -o den-float-test den-float-test.c

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/{bin,src/floattest}
cp floattest $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp floattest1 $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp den-float-test $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp floattest.c $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/src/floattest
cp floattest1.c $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/src/floattest
cp den-float-test.c $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/src/floattest

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


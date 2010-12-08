%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Dhrystone test package
Name            : dry
Version         : 2.2
Release         : 1
License         : Not distributable
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : Applications/Test
Source          : %{name}-%{version}.tar.bz2
Patch1          : dry-2.2-linux.patch
Patch2          : dry-2.2-stop-debug-output.patch
Patch3          : dry-2.2-mintime.patch
Patch4          : dry-2.2-exit.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
gcc -o dry1.o -c dry.c
gcc -DPASS2 dry.c dry1.o -o dry2
gcc -DREG -o dry2.o -c dry.c
gcc -DPASS2 -DREG dry.c dry2.o -o dry2nr


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/{bin,src/dhrystone}
cp dry2 dry2nr $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
cp dry.c $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/src/dhrystone

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


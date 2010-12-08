%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : BYTE Magazine's BYTEmark benchmark
Name            : nbench-byte
Version         : 2.2.2
Release         : 1
License         : Not distributable, Copyright CMP Media LLC.
Vendor          : Freescale
Packager        : Steve Papacharalambous
Group           : Applications/Test/Benchmark
Source          : %{name}-%{version}.tar.gz
Patch1          : nbench-byte-2.2.2-cross-compile.patch
Patch2          : nbench-byte-2.2.2-64bit-fix.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Linux/Unix port of release 2 of BYTE Magazine's BYTEmark benchmark program
(previously known as BYTE's Native Mode Benchmarks).

See: http://www.tux.org/~mayer/linux/bmark.html

Original program see: http://www.byte.com/bmark/bmark.htm

Copyright information: http://www.cmp.com/delivery/copyright.html


%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
make


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/opt/nbench
for i in nbench NNET.DAT
do 
    if [ -f $i ]
    then
        cp $i $RPM_BUILD_ROOT/%{pfx}/opt/nbench
    fi
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


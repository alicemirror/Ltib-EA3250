%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : gdb debugger for connecting to a BDM device (m68k)
Name            : m68k-gdb-bdm
Version         : 6.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Debuggers
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This is for use with the BDM dongle that is M54XX development boards.
The BDM is the "P & E Microcomputer" and communicates via the host
parallel port. 

The mode is:

CABLE_CFLV  Version F
ColdFire BDM Interface (Parallel Port, 3.3V)

The url is: http://www.pemicro.com/

%Prep
%setup 

%Build
export PATH=$UNSPOOF_PATH
make
cp m68k-linux-bdm-gdb/m68k-linux-gdb/bin/m68k-bdm-linux-gdb $TOP/bin/m68k-bdm-linux-gdb
cp 5485.gdb $TOP/bin/5485.gdb

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

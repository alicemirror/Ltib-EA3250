%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Rotates, compresses, removes and mails system log files.
Name            : logrotate
Version         : 3.7.4
Release         : 7
License         : GPL
Vendor          : UNKNOWN(Freescale)
Packager        : UNKNOWN(LTIB addsrpms)
Group           : System Environment/Base
URL             : UNKNOWN
Source          : logrotate-3.7.4.tar.gz
Patch1          : logrotate-selinux.patch
Patch2          : logrotate-fdLeak.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms

%Prep

%setup
#%patch1 -p1 -b .rhat
%patch2 -p1 -b .fdLeak


%Build
make RPM_OPT_FLAGS="-O2 -g"

%Install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT/%{pfx} MANDIR=/opt/freescale/ltib/usr/man install
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
mkdir -p $RPM_BUILD_ROOT/var/lib


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

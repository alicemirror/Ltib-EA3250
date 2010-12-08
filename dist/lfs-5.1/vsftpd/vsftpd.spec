%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : vsftpd - Very Secure Ftp Daemon
Name            : vsftpd
Version         : 2.0.5
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch1          : vsftpd-2.0.3-sysdeputil_uc.patch
Patch2          : vsftpd-2.0.5-syscall2.patch
Patch3          : vsftpd-2.0.5-config.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
make LIBS='-lcrypt'

%Install
rm -rf $RPM_BUILD_ROOT
for i in usr/sbin etc usr/share/man/man8 usr/share/man/man5 etc/xinetd.d usr/share/nobody usr/share/empty
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/$i
done
cp -a vsftpd          $RPM_BUILD_ROOT/%{pfx}/usr/sbin
cp -a vsftpd.conf     $RPM_BUILD_ROOT/%{pfx}/etc
cp -a vsftpd.8        $RPM_BUILD_ROOT/%{pfx}/usr/share/man/man8/vsftpd.8
cp -a vsftpd.conf.5   $RPM_BUILD_ROOT/%{pfx}/usr/share/man/man5/vsftpd.conf.5
cp -a xinetd.d/vsftpd $RPM_BUILD_ROOT/%{pfx}/etc/xinetd.d/vsftpd

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

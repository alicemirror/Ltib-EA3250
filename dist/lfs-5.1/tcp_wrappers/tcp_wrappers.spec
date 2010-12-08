%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A security tool which acts as a wrapper for TCP daemons
Name            : tcp_wrappers
Version         : 7.6
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Daemons
Source          : http://files.ichilton.co.uk/nfs/%{name}_%{version}.tar.gz
Patch0          : http://www.linuxfromscratch.org/patches/blfs/5.1/tcp_wrappers-7.6-shared-lib-plus-plus.patch
Patch1          : tcp_wrappers-7.6-uclibc.patch
Patch2          : tcp_wrappers-7.6-malloc.patch
Patch3          : tcp_wrappers-7.6-non-root.patch
Patch4          : tcp_wrappers-7.6-uclibc-strerror.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
if [ -n "$UCLIBC" ]
then 
    make REAL_DAEMON_DIR=/usr/sbin STYLE=-DPROCESS_OPTIONS linux-uclibc
else
    make REAL_DAEMON_DIR=/usr/sbin STYLE=-DPROCESS_OPTIONS linux
fi

%Install
rm -rf $RPM_BUILD_ROOT
for i in sbin lib include
do
    install -m 755 -d $RPM_BUILD_ROOT/%{pfx}/usr/$i
done
for i in man3 man5 man8
do
    install -m 755 -d $RPM_BUILD_ROOT/%{pfx}/usr/share/man/$i
done
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

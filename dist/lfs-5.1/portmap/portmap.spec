%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A program which manages RPC connections
Name            : portmap
Version         : 5beta
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Daemons
Source          : ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
Patch0          : http://www.linuxfromscratch.org/patches/blfs/5.1/portmap-5beta-compilation-fixes-2.patch
Patch1          : http://www.linuxfromscratch.org/patches/blfs/5.1/portmap-5beta-glibc-errno-fix.patch
Patch2          : portmap-5beta-non-root.patch
Patch3          : portmap-5beta-strerror.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : tcp_wrappers

%Description
%{summary}

%Prep
%setup -n  %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
if [ -n "$UCLIBC" ]
then
    make UCLIBC=y
else
    make
fi

%Install
rm -rf $RPM_BUILD_ROOT
for i in sbin usr/sbin
do
    install -m 755 -d $RPM_BUILD_ROOT/%{pfx}/$i
done
install -m 755 -d $RPM_BUILD_ROOT/%{pfx}/usr/share/man/man8
make install BASEDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

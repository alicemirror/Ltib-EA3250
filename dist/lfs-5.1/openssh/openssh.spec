%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The OpenSSH implementation of SSH protocol versions 1 and 2.
Name            : openssh
Version         : 4.3p2
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Internet
Source          : %{name}-%{version}.tar.gz
Source1         : openssh_hackable_keys.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%setup -T -D -a 1

%Build
LD=gcc ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}  --with-zlib=$DEV_IMAGE/usr --with-ssl-dir=$DEV_IMAGE/usr --with-ldflags="-L$DEV_IMAGE/lib" --config-cache

make -j1 sysconfdir=%{_sysconfdir}/ssh

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install sysconfdir=%{_sysconfdir}/ssh DESTDIR=$RPM_BUILD_ROOT/%{pfx}
if [ "$PKG_OPENSSH_WANT_HACKABLE_KEYS" = "y" ]
then
    cp -a hackable_keys/* $RPM_BUILD_ROOT/%{pfx}/etc/ssh/

fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(4755,root,root)  %{pfx}/usr/libexec/ssh-keysign
%{pfx}/*

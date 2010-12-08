%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Startup/Shutdown programs and scripts
Name            : sysvinit
Version         : 2.85
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : sysvinit-2.85.tar.gz
Patch1          : sysvinit-2.85-Makefile.patch
Patch2          : sysvinit-2.85-noinitctldev.patch
Patch3          : sysvinit-2.85-lcrypt.patch
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
make -C src

%Install
rm -rf $RPM_BUILD_ROOT
for i in sbin etc /usr/bin usr/share/man/man8 usr/share/man/man5 usr/share/man/man1 usr/include
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/$i
done
make -C src ROOT=$RPM_BUILD_ROOT/%{pfx} \
            BIN_OWNER=`id -u` BIN_GROUP=`id -g` install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



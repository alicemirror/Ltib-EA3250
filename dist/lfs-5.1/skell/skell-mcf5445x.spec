%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Skelleton files for an embedded root filesystem
Name            : skell
Version         : 1.13
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
Source          : %{name}-%{version}.tar.gz
Patch1          : skell-1.13-devfs_dhcp.patch
Patch2          : skell-1.13-www.patch
Patch3          : skell-1.12-20060407-smb.patch
Patch4          : skell-1.13-20060601-dhcp.patch
Patch5		: skell-1.13-udev-2.patch
Patch6		: mcf54455-demo-sysfiles-1.patch
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
%patch5 -p1
%patch6 -p1

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
cp -a * $RPM_BUILD_ROOT/%{pfx}
if [ -z "$PKG_SKELL_WANT_TERMINFO" ]
then
    rm -rf $RPM_BUILD_ROOT/%{pfx}/usr/share/terminfo
fi
# This file is patched into existence, so we have to
# explicitly set its permissions:
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/mount-proc-sys

ln -s /proc/mounts $RPM_BUILD_ROOT/%{pfx}/dev/mtab

# This can be removed once the patch for smb has been integrated
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/smb

# This can be removed once the patch for dhcp has been integrated
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/dhcp

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%attr(2777,root,ftp)  %{pfx}/var/ftp/pub
%attr(1777,root,root) %{pfx}/tmp
%attr(777,root,root)  %{pfx}/var/tmp
%attr(0666, root, root) %dev(c, 5, 1) %{pfx}/dev/console
%attr(0666, root, root) %dev(c, 1, 3) %{pfx}/dev/null
%attr(755,root,root)  %{pfx}/etc/rc.d/init.d/devfsd
%{pfx}/*

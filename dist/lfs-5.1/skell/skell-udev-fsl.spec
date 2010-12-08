%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Skelleton files for an embedded root filesystem
Name            : skell
Version         : 1.16
Release         : 2
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
Source          : %{name}-%{version}.tar.gz
Patch1		: skell-1.16-udev.patch
Patch2		: skell-1.13-depmod-modalias.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
cp -a * $RPM_BUILD_ROOT/%{pfx}
if [ -z "$PKG_SKELL_WANT_TERMINFO" ]
then
    rm -rf $RPM_BUILD_ROOT/%{pfx}/usr/share/terminfo
fi
ln -s /proc/mounts $RPM_BUILD_ROOT/%{pfx}/dev/mtab

# This can be removed once the patch for smb has been integrated
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/smb

# This can be removed once the patch for dhcp has been integrated
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/dhcp

# This can be removed once the patch for udev has been integrated
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/filesystems
chmod 755 $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/mount-proc-sys

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%attr(2777,root,ftp)  %{pfx}/var/ftp/pub
%attr(1777,root,root) %{pfx}/tmp
%attr(777,root,root)  %{pfx}/var/tmp
%attr(0666, root, root) %dev(c, 5, 0) %{pfx}/dev/tty
%attr(0666, root, root) %dev(c, 5, 1) %{pfx}/dev/console
%attr(0666, root, root) %dev(c, 1, 3) %{pfx}/dev/null
%attr(755,root,root)  %{pfx}/etc/rc.d/init.d/devfsd
%{pfx}/*

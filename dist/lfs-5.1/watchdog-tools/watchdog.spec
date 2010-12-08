%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Software watchdog for Linux
Name            : watchdog
Version         : 5.4
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Systems Administration
Source          : watchdog-%{version}.tar.gz
Patch1          : watchdog-fsl-config-2.patch
Patch2          : watchdog-fsl-daemon-3.patch
BuildRoot       : %{_tmppath}/%{name}-%{version}
Prefix          : %{pfx}

%Description
watchdog 5.4  
  by Michael Meskes (http://freshmeat.net/~meskes/)
  Fri, Aug 17th 2007 06:02 

About:
The Linux kernel can reset the system if serious problems are detected.
This can be implemented via special watchdog hardware, or via a slightly
less reliable software-only watchdog inside the kernel. Either way, there
needs to be a daemon that tells the kernel the system is working fine. If
the daemon stops doing that, the system is reset. watchdog is such a
daemon. It opens /dev/watchdog, and keeps writing to it often enough to
keep the kernel from resetting, at least once per minute. Each write
delays the reboot time another minute. After a minute the watchdog
hardware will cause the reset. In the case of a software watchdog, the
ability to reboot will depend on the state of the machines and interrupts. 

Changes:
Added "another-chance" repair script written by Erik Rossen Applied some
changes to RedHat init script. Added sysconf script for RedHat. Made
wd_keepalive honor config file option. Added wd_keealive manpage. Made
wd_keepalive not start without a watchdog device. Fixed some typos in
watchdog manpage. Updated Debian files. 

Release focus: Minor feature enhancements 
      License: GNU General Public License (GPL) 
  Project URL: http://freshmeat.net/projects/watchdog/
     Homepage: http://freshmeat.net/redir/watchdog/11306/url_homepage/watchdog
       Tar/GZ: http://freshmeat.net/redir/watchdog/11306/url_tgz/watchdog
Debian package: http://freshmeat.net/redir/watchdog/11306/url_deb/watchdog

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/sbin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
chmod 755 watchdog.script
cp -a src/wd_keepalive  $RPM_BUILD_ROOT/%{pfx}/usr/sbin
cp -a watchdog.script $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/watchdog
cp -a watchdog.conf $RPM_BUILD_ROOT/%{pfx}/etc

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

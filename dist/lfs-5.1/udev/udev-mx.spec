%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Userspace device files
Name            : udev
Version         : 091
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : admin
Source          : udev-%{version}.tar.bz2
Patch0		: udev_0.091-2.diff.gz
Patch1          : udev-091-startupscript.patch
Patch2          : udev-mx31_rules.patch
Patch3          : udev-mx31_event0.patch
Patch4          : udev-mx31_mtd.patch
Patch5          : udev-mx31_modalias.patch
Patch6		: udev-offsetof-fix.patch
Patch7		: udev-091-mx31-pmic-rtc.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
patch -p1 < debian/patches/enable_after_udev
patch -p1 < debian/patches/ifrename_wait_retry
patch -p1 < debian/patches/initramfs_quiet
patch -p1 < debian/patches/no_libsepol
patch -p1 < debian/patches/path_id_bashisms
patch -p1 < debian/patches/udev-synthesize-02.patch
patch -p1 < debian/patches/udev-synthesize-md
patch -p1 < debian/patches/udev-synthesize-waldi
patch -p1 < debian/patches/udev-synthesize-z80

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%Build
make udevdir=/dev V=true

%Install
rm -rf $RPM_BUILD_ROOT
make install udevdir=/dir DESTDIR=$RPM_BUILD_ROOT/%{pfx} V=true

install -d $RPM_BUILD_ROOT/%{pfx}/sbin
install -d $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/%{pfx}/etc/udev/scripts
install -d $RPM_BUILD_ROOT/%{pfx}/etc/hotplug.d/default

install extra/udev.startup $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/udev
install -m 755 udevsynthesize udevsend $RPM_BUILD_ROOT/%{pfx}/sbin

install -m 755 extra/*.sh extras/*.sh \
	       $RPM_BUILD_ROOT/%{pfx}/etc/udev/scripts

install -m 644 extra/links.conf \
           $RPM_BUILD_ROOT/%{pfx}/etc/udev/

sed -e 's/^#\([^ ]\)/\1/' < extra/compat.rules > \
           $RPM_BUILD_ROOT/%{pfx}/etc/udev/compat-full.rules

install -m 644 extra/10-mx31.rules \
	   $RPM_BUILD_ROOT/%{pfx}/etc/udev/rules.d

install -m 644 extra/udev.rules \
	   $RPM_BUILD_ROOT/%{pfx}/etc/udev/rules.d/50-udev.rules

install -m 644 extra/compat.rules \
	   $RPM_BUILD_ROOT/%{pfx}/etc/udev/rules.d/60-compat.rules

install -m 644 extra/devfs.rules \
	   $RPM_BUILD_ROOT/%{pfx}/etc/udev/rules.d/70-devfs.rules

ln -sfn /sbin/udevsend $RPM_BUILD_ROOT/%{pfx}/etc/hotplug.d/default/10-udev.hotplug

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

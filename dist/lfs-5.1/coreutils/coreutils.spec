%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : coreutils - GNU core utilities commonly used in shell scripts
Name            : coreutils
Version         : 6.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.bz2
Patch1          : coreutils-6.3-gcc-4.3.patch
Patch2          : coreutils-6.3-no-man.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

Provides        : sh-utils

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
# fu_cv_sys_stat_statfs2_bsize is needed to turn on df
utils_cv_sys_open_max=1019 fu_cv_sys_stat_statfs2_bsize=yes \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
# brutal, but more subtle attempts failed.
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/uptime
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/man/man1/uptime.1

# fix up paths to be compatible with busybox/fileutils/sh-utils etc
for i in bin sbin %_sbindir
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/$i
done
for f in stty pwd df sync echo ln cat chown rmdir ls uname touch true cp chmod sleep mkdir false date mv chgrp mknod dd rm
do
    mv $RPM_BUILD_ROOT/%{pfx}/%_bindir/$f $RPM_BUILD_ROOT/%{pfx}/%base/bin/$f
done
mv $RPM_BUILD_ROOT/%{pfx}/%_bindir/chroot $RPM_BUILD_ROOT/%{pfx}/%_sbindir/chroot


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



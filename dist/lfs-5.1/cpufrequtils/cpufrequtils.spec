%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : cpufreq utilities
Name            : cpufrequtils
Version         : 005
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille, John Faith
Group           : Applications/System
Source          : cpufrequtils-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://www.kernel.org/pub/linux/utils/kernel/cpufreq/cpufrequtils.html

%Description
%{summary}

%Prep
%setup

%Build
if [ ! -f Makefile.orig ]; then
	perl -p -i -e 's,^HOSTCC.*,HOSTCC = $ENV{BUILDCC},;' Makefile
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/usr/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


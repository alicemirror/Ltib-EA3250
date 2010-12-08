%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Timezone data and utilities
Name            : timezone
Version         : 2006n
Release         : 1
License         : Public Domain/BSD
Vendor          : Freescale
Packager        : John Faith
Group           : System Environment/Utilities
Source          : tzcode2006n.tar.gz
Source1         : tzdata2006n.tar.gz
Patch0          : timezone-2006n-make.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : ftp://elsie.nci.nih.gov/pub

%Description
%{summary}

%Prep
# Unpack both tar files.  Use '-c' since there is no top-level
# directory in the tarfiles.
%setup -c
%setup -T -D -a 1
%patch0 -p1

%Build
make  HOST_CC="$BUILDCC" TOPDIR=%{__prefix} TZDIR=%{_prefix}/share/zoneinfo ETCDIR=%{_prefix}/usr/bin

%Install
rm -rf $RPM_BUILD_ROOT

# Note: we deliberately don't install date, which comes from busybox/coreutils
make -j1 install MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man TZDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/zoneinfo TOPDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} ETCDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin

if [ "$PKG_TIMEZONE_WANT_LIBTZ" != "y" ]; then
	rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libtz.a
fi
if [ "$PKG_TIMEZONE_WANT_TZCODE" != "y" ]; then
	rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
fi

# cleanup paths to match glibc (zic,zdump)
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
for i in zic zdump
do
    test -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/$i && mv $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/$i $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/$i
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : linux atm bus related utilities.
Name            : linux-atm
Version         : 2.4.1
Release         : 1
License         : GPL/LGPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0          : linux-atm_2.4.1-17.diff
Patch1          : linux-atm-2.4.1-17-cross.patch
Patch2          : linux-atm-2.4.1-mkerrnos_pl.patch
Patch3          : linux-atm-2.4.1-uclibc-1.patch
Patch4          : linux-atm-2.4.1-types-h.patch
Patch5          : linux-atm-2.4.1-types-h-32.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n linux-atm-2.4.1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make HOSTCC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \
             MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man
mkdir -p $RPM_BUILD_ROOT/etc
install -c -m 644 src/config/hosts.atm $RPM_BUILD_ROOT/etc
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

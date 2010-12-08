%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : PCI bus related utilities.
Name            : pciutils
Version         : 2.2.4
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0          : %{name}-%{version}-85xx-PCIe.patch
Patch1          : %{name}-%{version}-fix-configure.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1

%Build

# This nonsense is needed cope with
# freescale-coldfire-m68k-linux-gnu-4.1-30.i686.rpm who's header
# files are not correctly sanitised
OPT="-O2"
if cpp -dM </dev/null | grep -q _mcoldfire_
then
    OPT="$OPT -DCONFIG_COLDFIRE"
fi
    
make -j1 sys=Linux cpu=${LINTARCH} PREFIX=%{_prefix} ZLIB=no OPT="$OPT"

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install PREFIX=%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \
             MANDIR=%{_prefix}/share/man

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

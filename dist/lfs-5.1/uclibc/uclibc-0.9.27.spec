%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define pkg_name uClibc
%define linux_libc_headers linux-libc-headers-2.4.29

Summary         : uClibc - a Small C Library for Linux
Name            : uclibc
Version         : 0.9.27
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{pkg_name}-%{version}.tar.bz2
Source1         : %{linux_libc_headers}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

See: http://www.uclibc.org/

%Prep
%setup -n uClibc-%{version}
tar jxvf %{SOURCE1}

%Build
if [ ! -e %{linux_libc_headers}/include/asm ] 
then
    cd %{linux_libc_headers}/include/
    ln -s asm-%{_target_cpu} asm
    cd -
fi
PKG_UCLIBC_PRECONFIG=${PKG_UCLIBC_PRECONFIG:-uclibc.config}
if [ -f "$PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG" ]
then
    cp $PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG .config
fi
if [ -n "$PKG_LIBC_WANT_CF" -o -n "$SCB_WANT_CF" ]
then
    make menuconfig HOSTCC="$BUILDCC"
    cp .config $PLATFORM_PATH/$PKG_UCLIBC_PRECONFIG
else
    yes "" | make config HOSTCC="$BUILDCC"
fi
make HOSTCC="$BUILDCC"


%Install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

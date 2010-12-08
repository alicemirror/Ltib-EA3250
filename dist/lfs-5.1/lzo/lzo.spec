%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : LZO is a portable lossless data compression library written in ANSI C.
Name            : lzo
Version         : 2.03
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : System Environment/Libraries
Source          : lzo-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
if [ "$GNUTARCH" = m68knommu ]
then
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	--disable-asm --disable-shared
else
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	--disable-asm --enable-shared
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

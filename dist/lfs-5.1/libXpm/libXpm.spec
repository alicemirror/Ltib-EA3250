%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 libXpm runtime library
Name            : libXpm
Version         : 3.5.7
Release         : 4
License         : MIT
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : System Environment/Libraries
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/lib/libXpm-3.5.7.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms libXpm-3.5.7-4.fc9.src.rpm

%Prep
%setup -q

%Build
./configure \
    --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	--disable-static
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

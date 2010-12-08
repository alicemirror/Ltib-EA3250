%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 libXaw runtime library
Name            : libXaw
Version         : 1.0.4
Release         : 2
License         : MIT/X11
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : System Environment/Libraries
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/lib/libXaw-1.0.4.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms libXaw-1.0.4-2.fc9.src.rpm

%Prep

%setup -q


%Build
./configure --disable-xaw8 --disable-static \
           --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
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

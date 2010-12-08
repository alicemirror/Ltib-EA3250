%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 libXxf86dga runtime library
Name            : libXxf86dga
Version         : 1.0.2
Release         : 2
License         : MIT/X11
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : System Environment/Libraries
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/lib/libXxf86dga-1.0.2.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms libXxf86dga-1.0.2-2.fc9.src.rpm

%Prep

%setup -q


%Build
%configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
           --enable-malloc0returnsnull
make


%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT%{pfx}

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_libdir}/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

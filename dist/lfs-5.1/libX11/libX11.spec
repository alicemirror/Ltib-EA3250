%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Lib X11
Name            : libX11
Version         : 1.1.5
Release         : 1
License         : X11
Vendor          : X.Org Foundation
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.x.org/
Source          : %{name}-%{version}.tar.bz2
Patch1          : libX11-1.1.5-1221162795.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires	: libxcb

%Description
This is the libX11 from XFree86.

%Prep
%setup
# patch needed for crosscompiling
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --enable-malloc0returnsnull
cd src/util
PATH=/usr/bin:/usr/local/bin:/bin make -e
cd ../..
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


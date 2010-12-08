%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : C++ debug Library
Name            : dbg
Version         : 1.20
Release         : 1
License         : LGPL
Vendor          : ltib.org
Packager        : Mike Goins
Group           : System Environment/Libraries
URL             : http://dbg.sourceforge.net/
Source          : %{name}-%{version}.tgz
Patch1          : dbg-1.20-1246985442.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
if g++ --version | perl -e '$_=<>; m,(\d\.\d),; exit($1 <= 3.3)'
then
    echo "$? dbg currently only builds with gcc up to version 3.3.x" 
    exit 1
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/lib/
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

# uncomment this if you want to install the test application 
#mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin/
#cp -a test-dbg  $RPM_BUILD_ROOT/%{pfx}/usr/bin/


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

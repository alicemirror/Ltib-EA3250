%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : FAAD decoder library
Name            : faad2
Version         : 2.6.1
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : John Faith
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0		: faad2-configure.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://sourceforge.net/project/showfiles.php?group_id=704

%Description
%{summary}

%Prep
%setup -n faad2
%patch0 -p1

%Build
chmod +x configure
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --with-mp4v2
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

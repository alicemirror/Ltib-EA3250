%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Clam AntiVirus is a GPL anti-virus toolkit for UNIX
Name            : clamav
Version         : 0.94
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch1          : clamav-0.88-configure-cross.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --disable-unrar --disable-clamav
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

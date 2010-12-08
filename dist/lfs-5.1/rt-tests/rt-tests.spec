%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Programs that test various rt-features
Name            : rt-tests
Version         : 0.19
Release         : 1
License         : GPLv2
Vendor          : Freescale
Packager        : Michael Barkowski
Group           : Development/Tools
URL             : git://git.kernel.org/pub/scm/linux/kernel/git/tglx/rt-tests.git
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/{bin,share/man/man8}
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

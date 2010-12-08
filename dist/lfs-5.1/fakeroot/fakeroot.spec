%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Fake root environment for packagers
Name            : fakeroot
Version         : 1.5.10
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : http://ftp.debian.org/debian/pool/main/f/fakeroot/fakeroot_1.5.10.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Used to let packagers build packages that have the attributes of root.  You
are never actually root so you avoid problems of accidentally blowing away
system files


%Prep
%setup


%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libfakeroot/*.la
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



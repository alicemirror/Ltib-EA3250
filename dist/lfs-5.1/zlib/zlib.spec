%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : zlib compression utilities and libraries
Name            : zlib
Version         : 1.2.3
Release         : 2
License         : zlib (Distributable)
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          : %{name}-%{version}.tar.bz2
Patch1          : zlib-1.2.3-arflags-1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --shared
mv Makefile Makefile.shared
./configure --prefix=%{_prefix}
mv Makefile Makefile.static
make -f Makefile.shared
make -f Makefile.static

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make -f Makefile.shared install prefix=${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}
make -f Makefile.static install prefix=${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



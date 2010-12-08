%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Benchmark suite for hard drive and file system performance
Name            : bonnie++
Version         : 1.93c
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Michael Barkowski
Group           : Testing
Source          : %{name}-%{version}.tgz
Patch1          : bonnie++-1.93c-getc_putc-cpp.patch
Patch2          : bonnie++-1.93c-gcc-4.3.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1 

%Build
# Stop configure script from trying to run things.
sed -i -e "s/AC_TRY_RUN/AC_TRY_COMPILE/" configure.in
autoconf
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install INSTALL=install prefix=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

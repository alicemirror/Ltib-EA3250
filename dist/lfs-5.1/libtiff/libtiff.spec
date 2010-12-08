%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library of functions for manipulating TIFF format image files
Name            : libtiff
Version         : 3.8.2
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : tiff-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n tiff-%{version}

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
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



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A tool for determining compilation options
Name            : pkgconfig
Version         : 0.21
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : pkg-config-%{version}.tar.gz
Patch0          : pkg-config-0.21-prefix_mungling.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n pkg-config-%{version}
%patch0 -p1

%Build
# don't add --build as glib will fail for a host build due to 
# stupid incorrect cross compile detection
./configure --prefix=%{_prefix} --host=$CFGHOST
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



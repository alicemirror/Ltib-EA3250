%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Libnet toolkit for construction/injection of network packets
Name            : libnet
Version         : 1.1.2.1
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : John Traill  
Group           : Applications/File
Source          : %{name}-%{version}.tar.gz
Patch1          : libnet-1.1.2.1-1189704364.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}
%patch1 -p1

%Build
ac_cv_libnet_endianess=big \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



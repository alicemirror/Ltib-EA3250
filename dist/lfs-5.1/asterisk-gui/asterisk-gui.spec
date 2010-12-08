%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Asterisk GUI
Name            : asterisk-gui
Version         : 2.0.4
Release         : 0
License         : GPL
Vendor          : Digium
Packager        : David Wu 
Group           : Applications/Communication
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Asterisk GUI


%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



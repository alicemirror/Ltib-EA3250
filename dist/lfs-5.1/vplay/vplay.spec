%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : vplay - vrec - mixer
Name            : vplay
Version         : 1.0
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Application/System
Source          : vplay-1.0.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n vplay

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/bin
cp vplay vrec $RPM_BUILD_ROOT/%{pfx}/bin

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*



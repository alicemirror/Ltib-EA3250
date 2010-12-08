%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Tool for extracting and viewing files in .zip archives.
Name            : unzip
Version         : 5.52
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/File
URL             : http://infozip.sourcforge.net
Source          : unzip552.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n unzip-5.52

%Build
make -f unix/Makefile linux_noasm
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

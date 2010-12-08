%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : text file browser, like more, but you can go back too.
Name            : less
Version         : 381
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : less-381.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
CC=gcc ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir='${prefix}/share/man'
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



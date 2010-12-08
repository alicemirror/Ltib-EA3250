%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A system-independent interface for user-level packet capture
Name            : libpcap
Version         : 0.8.3
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
ac_cv_linux_vers=2 \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --with-pcap=linux --enable-yydebug --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

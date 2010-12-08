%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library for supporting id3 tags
Name            : libid3tag
Version         : 0.15.1b
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : System Environment/Libraries
Source          : libid3tag-0.15.1b.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n libid3tag-0.15.1b

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
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

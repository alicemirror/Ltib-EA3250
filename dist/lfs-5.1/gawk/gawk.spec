%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : gawk - pattern scanning and processing language
Name            : gawk
Version         : 3.1.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Text
Source          : gawk-3.1.3.tar.bz2
Patch           : gawk-3.1.3-libexecdir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch -p1 


%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install bindir=%{base}/bin DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{base}/bin/*-
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
ln -s ../../bin/gawk $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/awk
ln -s ../../bin/gawk $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/gawk

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



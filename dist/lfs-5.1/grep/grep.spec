%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNU versions of grep pattern matching utilities
Name            : grep
Version         : 2.5.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Text
Source          : grep-2.5.1.tar.bz2
Patch1          : grep-2.5.1-symlinks.patch
Patch2          : grep-2.5.1-mempcpy.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-2.5
%patch1 -p1
%patch2 -p1

%Build
./configure --prefix=%{_prefix} --disable-perl-regexp --host=$CFGHOST \
--build=%{_build} --mandir=%{_mandir} --bindir=%{base}/bin
make

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : lfs-utils - miscellaneous programs to support LFS
Name            : lfs-utils
Version         : 0.3
Release         : 1
License         : BSD/UCB style license (distributable)
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : lfs-utils-0.3.tar.bz2
Patch0          : lfs-utils-0.3-strip.patch
Patch1          : lfs-utils-0.3-mktemp-config_update-1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
cd mktemp-1.5
sudo_cv_ebcdic=no \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir='${prefix}/share/man'
cd -
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} MANPREFIX='$(PREFIX)/share/man'
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/bin
mv $RPM_BUILD_ROOT/%{pfx}/%_bindir/mktemp $RPM_BUILD_ROOT/%{pfx}/%base/bin/mktemp

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : seq (from coreutils) - print a sequence of numbers
Name            : seq
Version         : 6.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : coreutils-%{version}.tar.bz2
Patch1          : coreutils-6.3-gcc-4.3.patch
Patch2          : coreutils-6.3-no-man.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n coreutils-%{version}
%patch1 -p1
%patch2 -p1

%Build
# fu_cv_sys_stat_statfs2_bsize is needed to turn on df
utils_cv_sys_open_max=1019 fu_cv_sys_stat_statfs2_bsize=yes \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make -C lib configmake.h
make -C lib libcoreutils.a
make -C src seq


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp -a src/seq $RPM_BUILD_ROOT/%{pfx}/usr/bin/seq

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/usr/bin/seq


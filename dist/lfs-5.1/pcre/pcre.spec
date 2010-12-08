%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Perl Regular Expression Library
Name            : pcre
Version         : 6.3
Release         : 1
License         : BSD License (revised)
Vendor          : Freescale
Packager        : Alan Tull
Group           : System Environment/Libraries
Source          : pcre-6.3.tar.gz
Patch1          : pcre-6.3-relink.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
./configure --prefix=%{_prefix}  --host=$CFGHOST --build=%{_build} --mandir=%{_mandir} --with-tags=CXX --with-gnu-ld

# This is needed to stop libtool using libstdc++.so from /usr/local/lib
perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool

make -j1 CC_FOR_BUILD="$BUILDCC" LINK_FOR_BUILD="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


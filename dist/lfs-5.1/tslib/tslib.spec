%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Abstraction layer for touchscreen panel events 
Name            : tslib
Version         : 1.0
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
Patch1          : tslib-1.0-enable_input_events.patch
Patch2		: tslib-1.0-mx-pre_gen-2.patch
Patch3          : tslib-1.0-directfb_link_fix.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 
%patch2 -p1 
%patch3 -p1

touch aclocal.m4
sleep 1
find . -name Makefile.in | xargs touch
sleep 1
touch configure

%Build
#sed -i s/AS_HELP_STRING/AC_HELP_STRING/ configure.ac
#./autogen.sh
chmod +x ./configure
export ac_cv_func_malloc_0_nonnull=yes
./configure CC=${TOOLCHAIN_PREFIX}gcc --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ts/*.la
# Remove unused platform binaries
for so in arctic2.so collie.so corgi.so h3600.so mk712.so; do
	rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/usr/lib/ts/$so
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

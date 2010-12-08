%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Font configuration and customization library
Name            : fontconfig
Version         : 2.4.2
Release         : 1
License         : MIT
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix		    : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
# we don't have docbook-utils in the distribution
ac_cv_prog_HASDOCBOOK=no \
ac_cv_prog_CC_FOR_BUILD="${BUILDCC}" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --with-arch=$GNUTARCH --sysconfdir=%{_sysconfdir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx} 
rm -rf $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

perl -pi -e 's,^</fontconfig>,
<dir>%{_prefix}/X11R6/lib/X11/fonts/TTF</dir>
<dir>%{_prefix}/X11R6/lib/X11/fonts/Type1</dir>
<dir>%{_prefix}/X11R6/lib/X11/fonts/truetype</dir>
</fontconfig>
,;
        ' $RPM_BUILD_ROOT/%{pfx}/%{_sysconfdir}/fonts/local.conf

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


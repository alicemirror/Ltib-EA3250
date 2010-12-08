%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The lrz and lsz modem communications programs.
Name            : lrzsz
Version         : 0.12.21
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Alan Tull
Group           : Applications/Communications
Source          : lrzsz_0.12.21.orig.tar.gz
Patch0          : lrzsz_0.12.21-4.diff
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n lrzsz-990823
%patch0 -p1

%Build
if [ -n "$UCLIBC" ]
then
    config_opts='ac_cv_lib_intl_gettext=no'
fi
eval $config_opts \
./configure --disable-pubdir \
            --enable-syslog \
            --program-transform-name=s/l// --cache-file=config.cache
touch Makefile.in
touch stamp-h.in
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*



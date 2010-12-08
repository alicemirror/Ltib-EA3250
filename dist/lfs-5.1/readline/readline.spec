%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Libraries to support command line editing functions
Name            : readline
Version         : 4.3
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Libraries
Source          : %{name}-%{version}.tar.gz
License         : GPL
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
cat <<TXT > config.cache
bash_cv_have_mbstate_t=\${bash_cv_have_mbstate_t=yes} > config.cache
TXT
./configure -C --prefix=%{_prefix} --host=$CFGHOST
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

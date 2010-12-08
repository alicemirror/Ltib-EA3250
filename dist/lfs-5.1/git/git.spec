%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Core git tools
Name            : git
Version         : 1.5.6.5
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
URL             : http://kernel.org/pub/software/scm/git/
Source0         : http://kernel.org/pub/software/scm/git/git-1.5.6.5.tar.gz
Patch0          : git-1.5.6.5-no-perl-install.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms git-1.5.6.5-1.fc9.src.rpm

%Prep
%setup -q
%patch0 -p1

%Build
config_opts='ac_cv_c_c99_format=yes ac_cv_fread_reads_directories=no ac_cv_snprintf_returns_bogus=no' 
eval $config_opts \
./configure  --prefix=%{_prefix} --host=$CFGHOST
make


%Install
rm -rf $RPM_BUILD_ROOT
make  DESTDIR=$RPM_BUILD_ROOT/%{pfx} install
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

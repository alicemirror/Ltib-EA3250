%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define pkg_name XML-Parser
%define build_root %(eval "`perl -e 'use Config; print$Config{installprefix} =~ m,(/[^/]+/[^/]+)/,; print $prefix'")

Summary         : XML Parser module for perl
Name            : xml-parser-pm
Version         : 2.34
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{pkg_name}-%{version}.tar.gz
License         : Perl (Artistic)
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup -n %{pkg_name}-%{version}

%Build
perl Makefile.PL 
make

%Install
rm -rf $RPM_BUILD_ROOT
make install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

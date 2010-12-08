%define pfx /opt/freescale/rootfs/%{_target_cpu}

# NOTE: perl is not relocatable as it encodes paths during the configure

Summary         : The Perl programming language
Name            : perl
Version         : 5.8.8
Release         : 1
License         : Artistic or GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
Source          : perl-5.8.8.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

# perl auto module dependency is pretty broken in rpm, so we have
# to turn off all dependency checks
Autoreqprov     : no


%Description
%{summary}

%Prep
%setup 

%Build
sh Configure -Dinstallprefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} -Dprefix=%{_prefix} -des -Accflags=-DNO_LOCALE 
make

%Install
rm -rf $RPM_BUILD_ROOT
make install

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

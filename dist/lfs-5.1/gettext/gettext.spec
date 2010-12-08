%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : GNU libraries and utilities for producing multi-lingual messages
Name            : gettext
Version         : 0.15
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
Patch0          : gettext-0.15-destdir.patch
Patch1          : gettext-error_print_progname.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
 --config-cache
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
# remove these 2 files to removed dependency on libgcj
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/gettext/gnu.gettext.DumpResource
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/gettext/gnu.gettext.GetURL
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



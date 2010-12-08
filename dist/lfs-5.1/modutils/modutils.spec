%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Kernel module management utilities
Name            : modutils
Version         : 2.4.25
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Kernel
Source          : %{name}-%{version}.tar.bz2
Patch0          : modutils-2.4.25-flex251.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1

%Build
export BUILDCC="$BUILDCC"
./configure --target=$CFGHOST --build=%{_build} --mandir='${prefix}/share/man'
make

%Install
rm -rf $RPM_BUILD_ROOT
make install exec_prefix=$RPM_BUILD_ROOT/%{pfx} prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



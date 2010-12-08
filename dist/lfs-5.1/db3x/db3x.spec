%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The Berkeley DB database library
Name            : db3x
Version         : 3.3.11
Release         : 1
License         : BSD variant
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : db-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Note: this library is not being used as it's license since 1.86 behaves
like GPL, and so anything linked against it has to be release open source

%Prep
%setup -n db-%{version}

%Build
cd build_unix
../dist/configure --prefix=%{_prefix} --enable-compat185
make 

%Install
rm -rf $RPM_BUILD_ROOT
cd build_unix
make prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} docdir=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/doc/db-3.3 install 
perl -pi -e 's,^DB185,DB,' $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/db_185.h

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



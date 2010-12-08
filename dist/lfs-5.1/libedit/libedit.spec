%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Editline library
Name            : libedit
Version         : 20070831
Release         : 2.10
License         : NetBSD
Vendor          : The Regents of the University of California
Packager        : Haiying Wang
Group           : System Environment/Libraries
Source          : %{name}-%{version}-%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}-%{release}

%Build
CFLAGS="%{optflags} -I$RPM_BUILD_ROOT/%{pfx}/include -L$RPM_BUILD_ROOT/%{pfx}/lib -fPIC"
%define optflags $CFLAGS
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
    --with-install-prefix=$RPM_BUILD_ROOT
make -j1 HOSTCC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx} 

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



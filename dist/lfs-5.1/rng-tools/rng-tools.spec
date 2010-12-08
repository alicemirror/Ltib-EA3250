%define pfx /opt/freescale/rootfs/%{_target_cpu}

%define argp_ver 1.3

Summary         : rngd - Check and feed random data from hardware device to kernel random device
Name            : rng-tools
Version         : 2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Kim Phillips
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Source1         : argp-standalone-%{argp_ver}.tar.gz
Patch0          : argp-standalone-1.3-throw.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -a 1 
%patch0

%Build
if [ -n "$UCLIBC" ]
then
    cd argp-standalone-%{argp_ver}
    ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
    make
    cd -
    CFLAGS="-O2 -Iargp-standalone-%{argp_ver}" \
    LDFLAGS="-Largp-standalone-%{argp_ver}" \
    LIBS="-largp" \
    ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
    make
else
    ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
    make
fi

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

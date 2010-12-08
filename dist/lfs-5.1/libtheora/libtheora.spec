%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The theora codec lib 
Name            : libtheora
Version         : 1.0 
Release         : 1
License         : BSD
Vendor          : Maxtrack
Packager        : Alan Carvalho de Assis
Group           : System Environment/Libraries
Source          : libtheora-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
if [ `echo "${PLATFORM}" | grep "mpc85"` ]
then
    E500_BSP="yes"
else
    E500_BSP="no"
fi

case "${PLATFORM}" in
    mpc8323eisr | mpc832x_rdb | mpc832xemds | mpc860fads | qs875s | tqm823l | zen)
        HARD_FP="no"
        ;;
    *)
        HARD_FP="yes"
        ;;
esac

HAVE_E500=${E500_BSP} \
HAVE_FPU=${HARD_FP} \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

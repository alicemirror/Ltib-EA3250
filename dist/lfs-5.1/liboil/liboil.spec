%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library of optimized inner loops
Name            : liboil
Version         : 0.3.11
Release         : 1
License         : Two-Clause BSD
Vendor          : Freescale
Packager        : Kurt Mahan
Group           : System Environment/Libraries
Source          : liboil-%{version}.tar.gz
Patch1          : liboil-0.3.11-e500-configure.patch
Patch2          : liboil-0.3.11-ppcfpu-configure.patch
Patch3          : liboil-0.3.11-noaltivec.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

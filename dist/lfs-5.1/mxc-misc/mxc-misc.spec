%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : platform specific unit tests for mxc platform
Name            : mxc-misc
Version         : 20070112
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Test
Source          : misc-mx-%{version}.tar.gz
Patch0		: misc-linux_2.6.19_fixup.patch
Patch1		: misc-remove_i2c.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n misc
%patch0 -p1
%patch1 -p1

%Build
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]
then
      KERNELDIR=$RPM_BUILD_DIR/linux
      KBUILD_OUTPUT=$KERNELDIR
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi
PLATFORM_UPPER="$(echo $PLATFORM | tr '[:lower:]' '[:upper:]')"
make PLATFORM=$PLATFORM_UPPER KBUILD_OUTPUT=$KBUILD_OUTPUT LINUXPATH=$KERNELDIR

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/unit_tests
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"
cp -rf platform/$PLATFORM_UPPER/* $RPM_BUILD_ROOT/%{pfx}/unit_tests/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(755,root,root)
%{pfx}/*

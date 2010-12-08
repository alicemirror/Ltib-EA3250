%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : platform specific unit tests for mxc platforms
Name            : mxc-test
Version         : 20080410
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Test
Source          : mxc-test-%{version}.tar.gz
Patch1          : mxc-test-20080410-rtic-script-install.patch
Patch2          : mxc-test-20080410-ioctl-check-2.patch
Patch3          : mxc-test-20080410-wdog_dev.patch
Patch4          : mxc-test-20080410-pmic_testapp.out.patch
Patch5          : mxc-test-20080410-fb-console.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%Build
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]; then
      KERNELDIR="$PWD/../linux-2.6.24"
      KBUILD_OUTPUT="$KERNELDIR"
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"

# Build modules
make -C module_test KBUILD_OUTPUT=$KBUILD_OUTPUT LINUXPATH=$KERNELDIR

# Build test apps
INCLUDE="-I$DEV_IMAGE/usr/src/linux/include \
-I$KERNELDIR/include \
-I$KERNELDIR/drivers/mxc/security/rng/include \
-I$KERNELDIR/drivers/mxc/security/sahara2/include"
make -j1 PLATFORM=$PLATFORM_UPPER INCLUDE="$INCLUDE" test

%Install
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]
then
      KERNELDIR="$PWD/../linux-2.6.24"
      KBUILD_OUTPUT="$KERNELDIR"
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"

rm -rf $RPM_BUILD_ROOT
# install modules
make -C module_test -j1 LINUXPATH=$KERNELDIR KBUILD_OUTPUT=$KBUILD_OUTPUT \
       DEPMOD=/bin/true INSTALL_MOD_PATH=$RPM_BUILD_ROOT/%{pfx} install

make PLATFORM=$PLATFORM_UPPER DESTDIR=$RPM_BUILD_ROOT/%{pfx}/unit_tests install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(755,root,root)
%{pfx}/*

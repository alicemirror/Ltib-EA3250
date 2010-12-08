
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : platform specific libraries for mxc platforms
Name            : mxc-lib
Version         : 20080410
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ross Wille
Group           : Test
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}

%Build
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]
then
      KERNELDIR="$PWD/../linux-2.6.24"
      KBUILD_OUTPUT=$KERNELDIR
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"

# Build libraries
INCLUDE="-I$DEV_IMAGE/usr/src/linux/include \
-I$KERNELDIR/include \
-I$KERNELDIR/drivers/mxc/security/rng/include \
-I$KERNELDIR/drivers/mxc/security/sahara2/include"
make -j1 PLATFORM=$PLATFORM_UPPER INCLUDE="$INCLUDE" all

%Install
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]
then
      KERNELDIR="$PWD/linux"
      KBUILD_OUTPUT="$PWD/linux"
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi

rm -rf $RPM_BUILD_ROOT
# install libraries and headers
make DEST_DIR=$RPM_BUILD_ROOT/%{pfx} install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(755,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utility for Ir devices
Name            : openobex
Version         : 1.2
Release         : 1
License         : GPL/LGPL
Vendor          : Freescale
Packager        : Rakesh S Joshi
Group           : Development/Libraries
Source          : %{name}-%{version}.tar.gz
Patch1          : openobex-1.2-fixpaths.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1

%Build
if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]
then
      KERNELDIR="$PWD/../linux"
      KBUILD_OUTPUT="$PWD/../linux"
else
      KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
      KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi
./configure --host=$CFGHOST --prefix=%{_prefix} --enable-apps -C --libdir="${DEV_IMAGE}/%{_prefix}"

if [ $TOOLCHAIN_PREFIX = "arm-none-linux-gnueabi-" ]
then
	sed -i "s,SUBDIRS = include lib apps ircp doc,SUBDIRS = include lib apps doc," Makefile
fi

make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Files
%defattr(-,root,root)
%{pfx}/*

%Clean
rm -rf $RPM_BUILD_ROOT/

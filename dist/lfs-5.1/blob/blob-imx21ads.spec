%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Blob bootloader firmware
Name            : blob
Version         : 2.0.5_pre2
Release         : 1
License         : GPL
Vendor          : Freescale Semiconductor
Packager        : John Faith
Group           : Applications/System
Source          : blob-2.0.5-pre2.tar.gz
Patch0          : blob.mx21-3.patch
Patch1          : blob.mx21-drive-strength-pcmcia.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://www.lart.tudelft.nl/lartware/blob/

%Description
%{summary}

%Prep
%setup -n blob-2.0.5-pre2
%patch0 -p1
%patch1 -p1
#makec
# Get build vars from config in PLATFORM_PATH
BLOB_BOARD=`grep '^CONFIG_BLOB_BOARD' $PLATFORM_PATH/.config | sed 's/^.*=//' | sed 's/"//g'`
ENABLE_NAND=""
if grep '^CONFIG_BLOB_NAND' $PLATFORM_PATH/.config; then
	ENABLE_NAND="--enable-nand"
fi

touch aclocal.m4
sleep 1
find . -name Makefile.in | xargs touch
sleep 1
touch configure
CC=arm-linux-gcc OBJCOPY=arm-linux-objcopy \
./configure \
  --with-linux-prefix=$DEV_IMAGE/usr/src/linux \
  --with-board=$BLOB_BOARD \
  --enable-maintainer-mode \
  --enable-md5 \
  --enable-net \
  --enable-debug \
  --host=i386 \
  $ENABLE_NAND \
  arm-unknown-linux-gnu

%Build
#makeb
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
cp src/blob/blob $RPM_BUILD_ROOT/%{pfx}/boot

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


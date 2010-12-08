%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : BlueZ bluetooth utilities
Name            : bluez-utils
Version         : 2.25
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch1          : bluez-utils-2.25-gcc-4.3.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
#  Determine whether certain libraries exist, and
#  what to tell ./configure about them.
if [ -f $DEV_IMAGE/usr/lib/libasound.so ] ; then
	_alsa_lib="--with-alsa=$DEV_IMAGE/usr/lib"
else
	_alsa_lib="--without-alsa"
fi

if [ -f $DEV_IMAGE/usr/lib/libusb.so ] ; then
	_usb_lib="--with-usb=$DEV_IMAGE/usr/lib"
else
	_usb_lib="--without-usb"
fi

./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	$_alsa_lib \
	$_usb_lib  \
	--without-openobex \
	--without-dbus \
	--without-fuse \
	--with-bluez=$DEV_IMAGE/usr/lib
make all

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make  install DESTDIR=${RPM_BUILD_ROOT}/%{pfx}

#  prefix=/usr is corrrect for the binaries, but /etc/* files 
#  end up being installed in /usr/etc.  Fix that.
mv  $RPM_BUILD_ROOT/%{pfx}/usr/etc  $RPM_BUILD_ROOT/%{pfx}

#  install the init script
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/default  $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
cp scripts/bluetooth.init $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/bluetooth
chmod +x $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/bluetooth

#  install config file
cp scripts/bluetooth.default $RPM_BUILD_ROOT/%{pfx}/etc/default/bluetooth

#  the installed pin helper is a python script, too heavyweight for
#  an embedded device.  replace it with a simple script:
cat > $RPM_BUILD_ROOT/%{pfx}/usr/bin/bluepin << EOF
#!/bin/sh
echo "PIN:123456"
EOF


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(644,root,root)  %{pfx}/etc/bluetooth/pin
%{pfx}/*


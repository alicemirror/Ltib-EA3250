%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Qtopia
Name            : qtopia-4
Version         : 4.3.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Rigby, John Faith
Group           : System Environment/Graphics
Source          : qtopia-opensource-src-%{version}.tar.gz
#Source1			: helix-20070404cvs.tar.bz2

# These patches can be platform specific but must be safe for application
# on all platforms
Patch1		: qtopia-opensource-4.3.0-qconfig-cursor-mouse-01.patch
#Patch2		: qtopia-opensource-4.3.0-rgb555-and-swapped-byte-video-01.patch
#Patch3		: qtopia-opensource-4.3.0-mpc5200-nogetospace-01.patch
Patch4		: qtopia-opensource-4.3.0-native-endian-audio-01.patch
Patch5		: qtopia-opensource-4.3.0-standard-touchscreen-01.patch
#Patch6		: qtopia-opensource-4.3.0-mpc5200-touchscreen-01.patch
Patch7		: qtopia-opensource-4.3.0-imx21-touchscreen-01.patch
Patch9		: qtopia-opensource-4.3.0-mx21-buttons-01.patch
Patch10		: qtopia-opensource-4.3.0-screensaver-01.patch
Patch11		: qtopia-opensource-4.3.0-mxc-platform-01.patch
#Patch12		: qtopia-opensource-4.3.0-mpc5200-platform-01.patch
Patch13		: qtopia-opensource-4.3.0-imx21-platform-01.patch
#Patch15		: qtopia-opensource-4.3.0-helix-build-01.patch
Patch16		: qtopia-opensource-4.3.0-gstreamer-01.patch
Patch17		: qtopia-opensource-4.3.0-usbkeyboard.patch
Patch18     : qtopia-opensource-4.3.0-video-playback-01.patch
Patch19		: qtopia-opensource-4.3.0-open_with_O_CREAT_fix.patch

BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -c qtopia-opensource-%{version}
cd qtopia-opensource-%{version}
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
#%patch12 -p1
%patch13 -p1
#%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1


# Options configurable in ltib
if [ -n "$PKG_QTOPIA_WANT_MEDIA_NONE" ]; then
	Q_MEDIA_CONFIG="-no-qtopiamedia"
elif [ -n "$PKG_QTOPIA_WANT_MEDIA_GSTREAMER" ]; then
	Q_MEDIA_CONFIG="-mediaengines gstreamer"
fi

if [ -n "$PKG_QTOPIA_WANT_SOUND_ALSA" ]; then
	Q_SOUND_CONFIG="-sound-system alsa"
elif [ -n "$PKG_QTOPIA_WANT_SOUND_OSS" ]; then
	Q_SOUND_CONFIG="-sound-system oss"
fi

if [ -z "$PKG_QTOPIA_WANT_IRDA" ]; then
	Q_IRDA_CONFIG="-no-infrared"
fi

# Define QWS_PLATFORM and specifiy extra qte and qpe configure options
export QWS_PLATFORM=$PLATFORM
case "$PLATFORM" in
	imx27ads | imx31ads | imx32ads)
	export QWS_PLATFORM=mxc
	# kbd-usb is used for the keypad too.
	export EXTRA_QTE_CONFIG=" -qt-mouse-tslib -qt-kbd-usb"
	#export EXTRA_QPE_CONFIG_HELIX=" -helix -helix-system-id linux-2.2-libc6-arm9-cross-gcc4 "
	export EXTRA_QPE_CONFIG=" -displaysize 240x320 $Q_SOUND_CONFIG $Q_MEDIA_CONFIG $Q_IRDA_CONFIG -no-drm -no-bluetooth -no-modem -no-sxe -no-voip -no-vpn"
	export QWS_KEYBOARD=USB:/dev/input/event0
	#export QWS_MOUSE_PROTO=Tslib:/dev/ts
	if [ _$QPE_USE_MOUSE = "_y" ]; then
		export QWS_MOUSE_PROTO="USB:/dev/input/mice"
	else
		export QWS_MOUSE_PROTO=Tslib:/dev/input/event1
	fi
	export QWS_DISPLAY=LinuxFb:mmWidth=54:mmHeight=72
	export QWS_SIZE="240x320"
	;;
	imx21ads)
	export EXTRA_QTE_CONFIG=
	#export EXTRA_QPE_CONFIG_HELIX=" -helix -helix-system-id linux-2.2-libc6-arm9-cross-gcc4 "
	export EXTRA_QPE_CONFIG=" -displaysize 240x320 $Q_SOUND_CONFIG $Q_MEDIA_CONFIG -no-drm -no-bluetooth -no-modem -no-sxe -no-voip -no-vpn"
	export QWS_KEYBOARD=imx21adskbdhandler
	export QWS_MOUSE_PROTO=imx21adsmousehandler
	export QWS_DISPLAY=LinuxFb:mmWidth=54:mmHeight=72
	export QWS_SIZE="240x320"
	;;
	imx25_3stack)
	export QWS_PLATFORM=mxc
	export EXTRA_QTE_CONFIG=" -qt-mouse-pc -qt-mouse-tslib -qt-kbd-usb"
	export EXTRA_QPE_CONFIG=" -displaysize 640x480 $Q_SOUND_CONFIG $Q_MEDIA_CONFIG $Q_IRDA_CONFIG -no-drm -no-bluetooth -no-modem -no-sxe -no-voip -no-vpn"
	export QWS_KEYBOARD=USB:/dev/input/keyboard0
	if [ _$QPE_USE_MOUSE = "_y" ]; then
		export QWS_MOUSE_PROTO=''
	else
		export QWS_MOUSE_PROTO=Tslib:/dev/input/ts0
	fi
	export QWS_DISPLAY=LinuxFb:mmWidth=108:mmHeight=88
	export QWS_SIZE="640x480"
	;;
	mpc5200)
	export EXTRA_QTE_CONFIG="-rgb555 -swapbytes_video "
	export EXTRA_QPE_CONFIG="-rgb555 -swapbytes-video -displaysize 1024x768"
	export QWS_KEYBOARD=TTY
	export QWS_DISPLAY=LinuxFb:mmWidth=170:mmHeight=125
	export QWS_SIZE="1024x768"
	;;
	mpc5121ads)
	# USB keyboard and mouse
	export EXTRA_QTE_CONFIG=" -qt-mouse-pc -qt-kbd-usb"
	export EXTRA_QPE_CONFIG=" -displaysize 1024x768 $Q_SOUND_CONFIG $Q_MEDIA_CONFIG -no-drm -no-bluetooth -no-modem -no-sxe -no-voip -no-vpn"
	export QWS_KEYBOARD=USB:/dev/input/event1
	export QWS_MOUSE_PROTO="IntelliMouse:/dev/input/mice"
	export QWS_DISPLAY=LinuxFb:mmWidth=170:mmHeight=125
	export QWS_SIZE="1024x768"
	;;
esac
export UC_QWS_PLATFORM=`perl -e "print uc $QWS_PLATFORM"`

# Create qtopia4 device config files
mkdir -p devices/$QWS_PLATFORM
CONFIG_PRI=devices/$QWS_PLATFORM/config.pri
if [ -f $CONFIG_PRI ]; then
	mv -f $CONFIG_PRI $CONFIG_PRI.bak
fi
echo "DEFINES+=QT_QWS_$UC_QWS_PLATFORM" > $CONFIG_PRI
echo "#DEFINES+=DEBUG" >> $CONFIG_PRI

# Use the target project file to disable applications.
# See src/general.pri for examples of what can be configured.
mkdir -p devices/$QWS_PLATFORM/src

{
 function NO { echo "PROJECTS-=$1"; }
 [ -z "$PKG_QTOPIA_WANT_APP_CALCULATOR" ]         && NO 'applications/calculator'
 [ -z "$PKG_QTOPIA_WANT_APP_CALENDAR" ]           && NO 'applications/datebook'
#[ -z "$PKG_QTOPIA_WANT_APP_CALLHISTORY" ]        && NO 'applications/callhistory'
 [ -z "$PKG_QTOPIA_WANT_APP_CAMERA" ]             && NO 'applications/camera'
 [ -z "$PKG_QTOPIA_WANT_APP_CLOCK" ]              && NO 'applications/clock'
 [ -z "$PKG_QTOPIA_WANT_APP_CONTACTS" ]           && NO 'applications/addressbook'
 [ -z "$PKG_QTOPIA_WANT_APP_GAMES" ]              && NO 'games/qasteroids games/fifteen games/minesweep games/snake'
 [ -z "$PKG_QTOPIA_WANT_APP_HELP" ]               && NO 'applications/helpbrowser'
 [ -z "$PKG_QTOPIA_WANT_APP_MAIL" ]               && NO 'applications/qtmail libraries/qtopiamail plugins/composers/email plugins/composers/generic plugins/composers/mms plugins/viewers/generic'
 [ -z "$PKG_QTOPIA_WANT_APP_MEDIAPLAYER" ]        && NO 'applications/mediaplayer'
 [ -z "$PKG_QTOPIA_WANT_APP_MEDIARECORDER" ]      && NO 'applications/mediarecorder'
 [ -z "$PKG_QTOPIA_WANT_APP_NOTES" ]              && NO 'applications/textedit'
 [ -z "$PKG_QTOPIA_WANT_APP_PACKAGEMANAGER" ]     && NO 'settings/packagemanager'
 [ -z "$PKG_QTOPIA_WANT_APP_PHOTOEDIT" ]          && NO 'applications/photoedit'
 [ -z "$PKG_QTOPIA_WANT_APP_SYNC" ]               && NO 'tools/qdsync/common tools/qdsync/app tools/qdsync/base tools/qdsync/pim'
 [ -z "$PKG_QTOPIA_WANT_APP_TODO" ]               && NO 'applications/todo'
 [ -z "$PKG_QTOPIA_WANT_APP_WORLDTIME" ]          && NO 'settings/worldtime'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_APPEARANCE" ]    && NO 'settings/appearance'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_CALIBRATE" ]     && NO 'settings/calibrate'
#[ -z "$PKG_QTOPIA_WANT_IRDA" ]                   && NO 'settings/beaming'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_DATETIME" ]      && NO 'settings/systemtime'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_HANDWRITING" ]   && NO 'settings/handwriting libraries/handwriting 3rdparty/plugins/inputmethods/pkim'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_HOMESCREEN" ]    && NO 'settings/homescreen'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_NETWORK" ]       && NO 'settings/network'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_LANGUAGE" ]      && NO 'settings/language'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_LOGGING" ]       && NO 'settings/logging'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_POWER" ]         && NO 'settings/light-and-power'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_SECURITY" ]      && NO 'settings/security'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_SERVERWIDGETS" ] && NO 'settings/serverwidgets'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_SPEEDDIAL" ]     && NO 'settings/speeddial'
 [ -z "$PKG_QTOPIA_WANT_SETTINGS_WORDS" ]         && NO 'settings/words'
 # Skip unneeded host tools
 [ -z "$PKG_QTOPIA_WANT_HOST_GUI_TOOLS" ]         && NO 'tools/qt/designer tools/qt/designer/src/uitools tools/qt/designer/src/lib tools/qt/designer/src/components tools/qt/assistant tools/qt/linguist'
 unset NO
} >> devices/$QWS_PLATFORM/projects.pri

DEVICE_CONFIGURE=devices/$QWS_PLATFORM/configure
echo "-arch $GNUTARCH -xplatform $QWS_PLATFORM -prefix /opt/Qtopia" > $DEVICE_CONFIGURE
#echo '-debug' >> $DEVICE_CONFIGURE
echo $EXTRA_QPE_CONFIG >> $DEVICE_CONFIGURE

# Define qt options in device qconfig.h (see main configure script).
if [ "$PKG_QTOPIA_WANT_MOUSE" = "y" ]; then
	cat > devices/$QWS_PLATFORM/qconfig.h << EOF
	#include "../../qtopiacore/qconfig-qpe.h"

	#ifdef QT_NO_CURSOR
	#undef QT_NO_CURSOR
	#endif
	#ifdef QT_NO_QWS_ALPHA_CURSOR
	#undef QT_NO_QWS_ALPHA_CURSOR
	#endif
	#ifdef QT_NO_QWS_CURSOR
	#undef QT_NO_QWS_CURSOR
	#endif

	#ifdef QT_NO_QWS_MOUSE
	#undef QT_NO_QWS_MOUSE
	#endif
	#ifdef QT_NO_QWS_MOUSE_AUTO
	#undef QT_NO_QWS_MOUSE_AUTO
	#endif
	#ifdef QT_NO_QWS_MOUSE_MANUAL
	#undef QT_NO_QWS_MOUSE_MANUAL
	#endif
EOF
fi

# Make platformdefs header
if [ ! -e devices/$QWS_PLATFORM/mkspecs/qws/linux-"$QWS_PLATFORM"-g++/qplatformdefs.h ]; then
	mkdir -p devices/$QWS_PLATFORM/mkspecs/qws/linux-"$QWS_PLATFORM"-g++
	cp -f devices/gcc411/mkspecs/linux-g++/qplatformdefs.h devices/$QWS_PLATFORM/mkspecs/qws/linux-"$QWS_PLATFORM"-g++/qplatformdefs.h
fi

echo export EXTRA_QPE_CONFIG=\"$EXTRA_QPE_CONFIG\" > ltibqtopiaconfig
echo export EXTRA_QTE_CONFIG=\"$EXTRA_QTE_CONFIG\" >> ltibqtopiaconfig
echo export PKG_QTOPIA_WANT_MOUSE=\"$PKG_QTOPIA_WANT_MOUSE\" >> ltibqtopiaconfig
echo export QWS_PLATFORM=$QWS_PLATFORM >> ltibqtopiaconfig
echo export QWS_KEYBOARD=\"$QWS_KEYBOARD\" >> ltibqtopiaconfig
echo export QWS_DISPLAY=\"$QWS_DISPLAY\" >> ltibqtopiaconfig
echo export QWS_SIZE=\"$QWS_SIZE\" >> ltibqtopiaconfig
echo export QWS_MOUSE_PROTO=\"$QWS_MOUSE_PROTO\" >> ltibqtopiaconfig

echo Note that e2fsprogs-devel, libjpeg/libjpeg-devel, uuid-dev/libuuid,
echo gettext \(msgfmt\), and libxtst-dev packages are required on the host.

# qmake config
# Use linux-arm-g++ configuration as a starting point, then substitute TOOLCHAIN_PREFIX
# and add target include, library paths.
cp -r qtopiacore/qt/mkspecs/qws/linux-arm-g++ qtopiacore/qt/mkspecs/qws/linux-$QWS_PLATFORM-g++
perl -p -i -e 's,arm-linux-,$ENV{TOOLCHAIN_PREFIX},;
               s,^((?:QMAKE|TMAKE)_CFLAGS\s+).*,$1 = -pipe -I. -I $ENV{DEV_IMAGE}/usr/include $ENV{EXTRA_CFLAGS},;
               s,^((?:QMAKE|TMAKE)_LFLAGS\s+).*,$1 = -L $ENV{DEV_IMAGE}/usr/lib $ENV{EXTRA_LDFLAGS},;
               s,^((?:QMAKE|TMAKE)_CXXFLAGS\s+.*),$1 $ENV{EXTRA_CFLAGS},;
              ' qtopiacore/qt/mkspecs/qws/linux-$QWS_PLATFORM-g++/qmake.conf

# Device qmake.conf
if [ ! -e devices/$QWS_PLATFORMmkspecs/qws/linux-$QWS_PLATFORM-g++/qmake.conf ]; then
	cp devices/imx21ads/mkspecs/qws/linux-imx21ads-g++/qmake.conf devices/$QWS_PLATFORM/mkspecs/qws/linux-$QWS_PLATFORM-g++
	perl -p -i -e 's,arm-linux-,$ENV{TOOLCHAIN_PREFIX},;
               s,^((?:QMAKE|TMAKE)_CFLAGS\s+).*,$1 = -pipe -I. -I $ENV{DEV_IMAGE}/usr/include $ENV{EXTRA_CFLAGS},;
               s,^((?:QMAKE|TMAKE)_LFLAGS\s+).*,$1 = -L $ENV{DEV_IMAGE}/usr/lib $ENV{EXTRA_LDFLAGS},;
               s,^((?:QMAKE|TMAKE)_CXXFLAGS\s+.*),$1 $ENV{EXTRA_CFLAGS},;
               s,IMX21ADS,$ENV{UC_QWS_PLATFORM},g;
              ' devices/$QWS_PLATFORM/mkspecs/qws/linux-$QWS_PLATFORM-g++/qmake.conf
fi

# Create generic q/s/l/q/custom-linux-$QWS_PLATFORM-g++.* files if not created by a patch
export QT_BASE=src/libraries/qtopiabase
test -e $QT_BASE/custom-linux-$QWS_PLATFORM-g++.h \
	|| cp $QT_BASE/custom-linux-generic-g++.h $QT_BASE/custom-linux-$QWS_PLATFORM-g++.h
test -e $QT_BASE/custom-linux-$QWS_PLATFORM-g++.cpp \
	|| cp $QT_BASE/custom-linux-generic-g++.cpp $QT_BASE/custom-linux-$QWS_PLATFORM-g++.cpp

# Symlink to helix source
#cd src/3rdparty/libraries/helix
#ln -s ../../../../../helix-20070404cvs src

# Create build dir
mkdir ../build

exit 0


%Build
cd build
QSRC=../qtopia-opensource-%{version}
. $QSRC/ltibqtopiaconfig

export PATH=$UNSPOOF_PATH
# Unset compiler to prevent gcc being used when the cross
# tools should be used. (Trolltech issue# 138807)
unset CC CXX
if [ "$EXTRA_QTE_CONFIG" = "" ] ; then
	echo yes | $QSRC/configure -device $QWS_PLATFORM -verbose
else
	echo yes | $QSRC/configure -device $QWS_PLATFORM -verbose -extra-qtopiacore-config "${EXTRA_QTE_CONFIG} -I ${DEV_IMAGE}/usr/include -L ${DEV_IMAGE}/usr/lib"
fi

# For debugging
export VERBOSE_SHELL=1

# Build root env var required by helix
#export BUILD_ROOT=$RPM_BUILD_DIR/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/src/3rdparty/libraries/helix/helixbuild/build
make -j1

exit 0


%Install
cd build
QSRC=../qtopia-opensource-%{version}
. $QSRC/ltibqtopiaconfig

export PATH=$UNSPOOF_PATH
echo creating qtopia install image
make install > /dev/null
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{pfx}/opt/Qtopia
cp -a image/* $RPM_BUILD_ROOT/%{pfx}/opt/Qtopia
install -d $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d

initscript=$RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/qtopia
cat > $initscript << EOF
#!/bin/sh
#
# Copyright 2006-2008, Freescale Semiconductor Inc.
#
if [ "\$1" = "stop" -o "\$1" = "restart" ]
then
    echo "Stopping qtopia: "
    killall qpe 2>/dev/null
    killall quicklauncher 2>/dev/null
    killall mediaserver 2>/dev/null
    killall mediaplayer 2>/dev/null
    killall sipagent 2>/dev/null
    killall sxemonitor 2>/dev/null
fi
if [ "\$1" = "stop" ]; then
	exit 0
fi
HOME=/root
# Set QPE_USE_MOUSE to "y" to use mouse 
# otherwise touchscreen will be used
QPE_USE_MOUSE="$PKG_QTOPIA_WANT_MOUSE"
export HOME QPE_USE_MOUSE
# Make sure usb input, mouse, and ts nodes exist
mkdir -p /dev/input
test -c /dev/input/event1 || mknod /dev/input/event1 c 13 65
test -c /dev/input/mice || mknod /dev/input/mice c 13 63
test -c /dev/ts || mknod /dev/ts c 11 0
if [ -c /dev/vc/0 ]; then
        qconsole=/dev/vc/0
elif [ -c /dev/tty0 ]; then
        qconsole=/dev/tty0
fi
# Disable screen blanking
if [ -n "\$qconsole" ]; then
	echo -e -n '\033[9]' > \$qconsole
fi
QTDIR=/opt/Qtopia
QPEDIR=/opt/Qtopia
LD_LIBRARY_PATH=/opt/Qtopia/lib
PATH=/opt/Qtopia/bin:\$PATH
QWS_SIZE="$QWS_SIZE"
export QTDIR QPEDIR LD_LIBRARY_PATH PATH QWS_SIZE
QWS_KEYBOARD="$QWS_KEYBOARD"
export QWS_KEYBOARD
QWS_MOUSE_PROTO="$QWS_MOUSE_PROTO"
export QWS_MOUSE_PROTO
if [ _\$QPE_USE_MOUSE = "_y" ]
then
	# Override pointer calibration when using mouse
	touch /etc/pointercal 
else
	# Hide mouse cursor when using touchscreen
	QWS_HIDE_CURSOR="Yes"
	export QWS_HIDE_CURSOR
	# Hide console cursor
	if [ -n "\$qconsole" ]; then
		echo -e -n '\033[?25l' > \$qconsole
	fi
	# Remove pointercal if it is empty
	[ -f /etc/pointercal -a ! -s /etc/pointercal ] && rm -f /etc/pointercal
fi
QWS_DISPLAY="$QWS_DISPLAY"
if [ -n "\$qconsole" ]; then
        QWS_DISPLAY="\$QWS_DISPLAY:tty=\$qconsole"
fi
export QWS_DISPLAY

#export QT_DEBUG_PLUGINS=1

cd /opt/Qtopia/bin
./qpe > /dev/null 2>&1 &
#./qpe &

# Calibration
if [ ! -f /etc/pointercal ]; then
	# qpe4 does not auto start calibration, so wait for qpe to start
	# then launch calibration.
	maxTries=6
	success=`expr \$maxTries + 4`
	try=1
	while [ \$try -lt \$maxTries ]
	do
		echo " Waiting for qcop (try \$try)..."
		# See if qcop is runnable
		qcop list >/dev/null 2>&1
		if [ "\$?" -eq 0 ]; then
			try=\$success
			break
		else
			try=\`expr \$try + 1\`
			sleep 1
		fi
	done
	# Request calibration
	if [ "\$try" -eq \$success ]; then
		echo " Requesting calibration"
		qcop service send Launcher "execute(QString)" "calibrate"
		#ln -s $HOME/Settings/pointercal /etc/pointercal
	else
		echo Failed to run touchscreen calibration since qcop could not run.
	fi
fi
EOF

chmod 744 $initscript
echo '1' > $RPM_BUILD_ROOT/%{pfx}/etc/firstuse
# setup Storage.conf
install -d $RPM_BUILD_ROOT/%{pfx}/root/Settings
cat > $RPM_BUILD_ROOT/%{pfx}/root/Settings/Storage.conf << EOF
[rootfs]
Name = Internal Storage
Removeable = 0
[/dev/sda1]
Name = USB Flash Drive
Removable = 1
EOF

# Make sure the strip scripts are run cross
export PATH=$SPOOF_PATH

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



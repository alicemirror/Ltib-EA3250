%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Utilities for infrared communication between devices
Name            : irattach
Version         : 0.9.18
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System/Servers
Source          : irda-utils-%{version}.tar.gz
URL             : http://sourceforge.net/projects/irda
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This spec file only builds irattach from irda-utils

%Prep
%setup -n irda-utils-%{version}

%Build
make -C irattach SYS_INCLUDES= SYS_LIBPATH= CC=gcc LD=ld

%Install
rm -rf $RPM_BUILD_ROOT

if [ -z $SYSCFG_IRDA_SERIAL_PORT ]; then
	echo SYSCFG_IRDA_SERIAL_PORT not defined
	exit 1
fi

mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/sbin
make -C irattach install ROOT=$RPM_BUILD_ROOT/%{pfx}

# IrDA init
IRDA_DEVICE=$SYSCFG_IRDA_SERIAL_PORT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/var/lock/subsys
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
initscript=$RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/irda
cat > $initscript << EOF
#!/bin/sh
#
# irda      This starts and stops IrDA
# Generated in irattach.spec 
#
[ -f /usr/sbin/irattach ] || exit 0
case "\$1" in
	start)
		# Attach irda device
		echo -n "Starting IrDA: "
		/usr/sbin/irattach $IRDA_DEVICE -s
		touch /var/lock/subsys/irda
		echo
		;;
	stop)
		# Stop service
		echo -n "Shutting down IrDA: "
		killall irattach
		rm -f /var/lock/subsys/irda
		echo
		;;
	restart)
		\$0 stop
		\$0 start
	*)
		echo "Usage: \$0 {start|stop|restart}"
		exit 1
esac
exit 0
EOF
chmod 744 $initscript

%Clean
rm -rf $RPM_BUILD_ROOT
# $RPM_BUILD_DIR/file.list.%{name}

%Files
%defattr(-,root,root,0755)
%{pfx}/*

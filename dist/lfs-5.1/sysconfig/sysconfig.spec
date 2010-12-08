%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: System configuration package
Name		: sysconfig
Version		: 1.2
Release		: 2
License		: GPL
Vendor		: Freescale
Packager	: Stuart Hughes
Group		: System Environment/Base
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

%Prep
#%setup

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d

if [ "$SYSCFG_START_SYSLOG" = "y" ]
then
    syslog=syslog
fi
if [ "$SYSCFG_START_UDEV" = "y" ]
then
    udev=udev
fi
if [ "$SYSCFG_START_MDEV" = "y" ]
then
    mdev=mdev
fi
if [ "$SYSCFG_START_DEVFSD" = "y" ]
then
    devfsd=devfsd
fi
if [ "$SYSCFG_START_NETWORK" = "y" ]
then
    network=network
fi
if [ "$SYSCFG_START_INETD" = "y" ]
then
    inetd=inetd
fi
if [ "$SYSCFG_START_PORTMAP" = "y" ]
then
    portmap=portmap
fi
if [ "$SYSCFG_START_DROPBEAR_SSH" = "y" ]
then
    dropbear=dropbear
fi
if [ "$SYSCFG_START_SSHD" = "y" ]
then
    sshd=sshd
fi
if [ "$SYSCFG_START_BOA" = "y" ]
then
    boa=boa
fi
if [ "$SYSCFG_SETTIME" = "y" ]
then
    settime=settime
fi
if [ "$SYSCFG_START_DHCPD" = "y" ]
then
    dhcpd=dhcp
fi
if [ "$SYSCFG_START_SAMBA" = "y" ]
then
    smb=smb
fi
if [ "$SYSCFG_START_QTOPIA" = "y" ]
then
	qtopia=qtopia
fi
if [ "$SYSCFG_START_WATCHDOG" = "y" ]
then
	watchdog=watchdog
fi
if [ "$SYSCFG_START_GTK2" = "y" ]
then
	gtk2=gtk2
fi
if [ "$SYSCFG_START_PANGO" = "y" ]
then
	pango=pango
fi

cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.conf
all_services="mount-proc-sys mdev udev hostname devfsd depmod modules filesystems syslog network inetd portmap dropbear sshd boa smb dhcpd settime qtopia watchdog gtk2 pango"
all_services_r="pango gtk2 watchdog qtopia settime dhcpd smb boa sshd dropbear portmap inetd network syslog filesystems modules depmod devfsd hostname udev mdev mount-proc-sys"

cfg_services="mount-proc-sys $mdev $udev hostname $devfsd depmod modules filesystems $syslog $network $inetd $portmap $dropbear $sshd $boa $smb $dhcpd $settime $qtopia $watchdog $gtk2 $pango"

cfg_services_r="$pango $gtk2 $watchdog $qtopia $settime $dhcpd $smb $boa $sshd $dropbear $portmap $inetd $network $syslog filesystems modules depmod $devfsd hostname $udev $mdev mount-proc-sys"

export HOSTNAME="${SYSCFG_HOSTNAME:-$PLATFORM}"
export NTP_SERVER="$SYSCFG_NTP_SERVER"
export MODLIST="$SYSCFG_MODLIST"
export RAMDIRS="$SYSCFG_RAM_DIRS"
export TMPFS="$SYSCFG_TMPFS"
export TMPFS_SIZE="${SYSCFG_TMPFS_SIZE:-512k}"
export READONLY_FS="$SYSCFG_READONLY_FS"
export INETD_ARGS="$SYSCFG_INETD_ARGS"
export BOA_ARGS="$SYSCFG_BOA_ARGS"
export SMBD_ARGS="${SYSCFG_SMBD_ARGS}"
export NMBD_ARGS="${SYSCFG_NMBD_ARGS}"
export DHCP_ARG="${SYSCFG_DHCP_ARG}"
export DEPLOYMENT_STYLE="${SYSCFG_DEPLOYMENT_STYLE:-NFS}"
export SYSCFG_DHCPC_CMD="${SYSCFG_DHCPC_CMD:-udhcpc -b -i }"
export DROPBEAR_ARGS="${SYSCFG_DROPBEAR_ARGS}"
EOF

# network interfaces
for i in 0 1 2 3 4 5
do
    if [  "$(eval echo \$$(echo SYSCFG_IFACE$i))" = "y" ]
    then
	if [ "$(eval echo \$$(echo SYSCFG_DHCPC$i))" = "y" ]
	then
	    cat <<EOF >> $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.conf
# net interface $i
export $(echo SYSCFG_IFACE$i)=y
export $(echo INTERFACE$i)="$(eval echo \$$(echo SYSCFG_NET_INTERFACE$i))"
export $(echo IPADDR$i)="dhcp"
EOF
	else
	    cat <<EOF >> $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.conf
# net interface $i
export $(echo SYSCFG_IFACE$i)=y
export $(echo INTERFACE$i)="$(eval echo \$$(echo SYSCFG_NET_INTERFACE$i))"
export $(echo IPADDR$i)="$(eval echo \$$(echo SYSCFG_IPADDR$i))"
export $(echo NETMASK$i)="$(eval echo \$$(echo SYSCFG_NET_MASK$i))"
export $(echo BROADCAST$i)="$(eval echo \$$(echo SYSCFG_NET_BROADCAST$i))"
export $(echo GATEWAY$i)="$(eval echo \$$(echo SYSCFG_NET_GATEWAY$i))"
export $(echo NAMESERVER$i)="$(eval echo \$$(echo SYSCFG_NAMESERVER$i))"
EOF
	fi
    fi
done

if [ "$PKG_BUSYBOX" = "y" -a "$PKG_SYSVINIT" != "y" ]
then
    # BusyBox init
    if [ "$SYSCFG_WANT_LOGIN_TTY" = "y" ]
    then
	sys_login=`echo "$SYSCFG_LOGING_TTY" | sed 's/\\\\\\\\n/\n/'`
    else
	sys_login="::respawn:-/bin/sh"
    fi
    cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/inittab
# see busybox-1.00rc2/examples/inittab for more examples
::sysinit:/etc/rc.d/rcS
$sys_login
::ctrlaltdel:/sbin/reboot
::shutdown:/etc/rc.d/rcS stop
::restart:/sbin/init
EOF
else
    # SysVInit
    if [ "$SYSCFG_WANT_LOGIN_TTY" = "y" ]
    then
	run_level=3
    else
	run_level=1
    fi
    cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/inittab
id:$run_level:initdefault:

si::sysinit:/etc/rc.d/rcS start

# Runlevel 0 is halt
# Runlevel 1 is single-user
# Runlevels 2-5 are multi-user
# Runlevel 6 is reboot

l0:0:wait:/etc/rc.d/rcS stop
l1:1:respawn:/bin/sh -i
l6:6:wait:/sbin/reboot

co:2345:respawn:${SYSCFG_LOGING_TTY:-$INITTAB_LINE}

ca::ctrlaltdel:/sbin/reboot
EOF
fi

cat <<'EOF' > $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.local
#!/bin/sh
#
# This script will be executed *after* all the other init scripts.
# You can put your own initialization stuff in here
if [ -x "/usr/bin/rpm" -a -e "/tmp/ltib" ]
then
    echo "rebuilding rpm database"
    rm -rf /tmp/ltib
    rpm --rebuilddb
fi

# fix up permissions
if [ -d /home/user ]
then
    chown -R user.user /home/user
fi

# Add nodes when running under the hypervisor and static devices
if [ -r /sys/class/misc/fsl-hv/dev -a ! -r /dev/fsl-hv ]
then
   echo "creating hypervisor nodes"
   DEVID=`cat /sys/class/misc/fsl-hv/dev`
   if [ -n "$DEVID" ]
   then
       MAJOR="${DEVID%%:*}"
       MINOR="${DEVID##*:}"

       if [ \( "$MAJOR" -gt 0 \) -a \( "$MINOR" -gt 0 \) ]
       then
	   rm -f /dev/fsl-hv
	   mknod /dev/fsl-hv c $MAJOR $MINOR
       fi
   fi
   for i in 0 1 2 3 4 5 6 7
   do
       mknod /dev/hvc$i c 229 $i
   done
fi

# add the fm device nodes
if [ -n "$(cat /proc/devices | grep fm | sed 's/\([0-9]*\).*/\1/')" -a ! -r /dev/fm0 ]
then
    if [ -d "/usr/share/doc/fmd-uspace-01.01/test" ]
    then
        echo "creating fman device nodes"
        cd /usr/share/doc/fmd-uspace-01.01/test
        sh fm_dev_create
        cd - >/dev/null
    fi
fi

EOF
chmod +x $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.local

# The kernel attempts to run /init (not /sbin/init!) from initramfs images
if [ "$SYSCFG_DEPLOYMENT_STYLE" = "INITRAMFS" ]
then
    ln -s /sbin/init $RPM_BUILD_ROOT/%{pfx}/init
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

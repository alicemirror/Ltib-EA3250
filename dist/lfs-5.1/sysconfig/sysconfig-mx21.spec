%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : System configuration package
Name            : sysconfig
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
#Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
#%setup -n %{name}-%{version}

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d

if [ "$SYSCFG_START_SYSLOG" = "y" ]
then
    syslog=syslog
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
    dhcpd=dhcpd
fi
if [ "$SYSCFG_START_IRDA" = "y" ]
then
    irda=irda
fi
if [ "$SYSCFG_START_SAMBA" = "y" ]
then
    smb=smb
fi
if [ "$SYSCFG_START_HARDWARETEST_DPM" = "y" ]
then
    dpmutils=dpmutils
fi
if [ "$SYSCFG_START_QTOPIA" = "y" ]
then
	qtopia=qtopia
fi


cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/rc.conf
all_services="hostname mount-proc-sys udev filesystems syslog depmod modules network settime inetd portmap dropbear boa dhcpd dpmutils irda qtopia"
all_services_r="qtopia irda dpmutils dhcpd boa dropbear portmap inetd settime network modules depmod syslog filesystems hostname"

cfg_services="hostname mount-proc-sys udev filesystems $syslog depmod modules $network $settime $inetd $portmap $dropbear $boa $chcpd $dpmutils $irda $qtopia"
cfg_services_r="$qtopia $irda $dpmutils $dhcpd $boa $dropbear $portmap $inetd $settime $network modules depmod $syslog filesystems hostname"

export HOSTNAME="${SYSCFG_HOSTNAME:-freescale}"
export NTP_SERVER="$SYSCFG_NTP_SERVER"
export MODLIST="$SYSCFG_MODLIST"
export RAMDIRS="$SYSCFG_RAM_DIRS"
export TMPFS="$SYSCFG_TMPFS"
export READONLY_FS="$SYSCFG_READONLY_FS"
export SYSLOG_SOCKET_FILE="$SYSCFG_SYSLOG_SOCKET_FILE"
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

if [ "$SYSCFG_WANT_LOGIN_TTY" = "y" ]
then
    sys_login="$SYSCFG_LOGING_TTY"
else
    sys_login="::respawn:-/bin/sh"
fi
cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/inittab
# see busybox-1.00rc2/examples/inittab for more examples
::sysinit:/etc/rc.d/rcS
$sys_login
::ctrlaltdel:/sbin/reboot
::shutdown:/etc/rc.d/rcS stop
::shutdown:/bin/umount -a -r
::shutdown:/sbin/swapoff -a
::restart:/sbin/init
::once:/usr/bin/demo_launcher
EOF


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


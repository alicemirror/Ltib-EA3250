%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Linux Wireless LAN
Name            : linux-wlan-ng
Version         : 0.1.12
Release         : 1
License         : MPL
Vendor          : Freescale
Packager        : John Faith
Group           : System Environment/Utilities
Source          : linux-wlan-ng-0.1.12.tar.gz
Patch0          : wlan-0.1.12-mx21-1.patch
Patch1          : wlan-0.1.12-iobase.patch
Patch2          : wlan-0.1.12-host-cc.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
Url             : http://www.linux-wlan.com

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
KERNEL_SRC_DIR=${RPM_BUILD_DIR}/linux
PCMCIA_SRC_DIR=${RPM_BUILD_DIR}/pcmcia-cs-3.2.4
# Check that kernel and pcmcia sources are available
if [ ! -d ${KERNEL_SRC_DIR} -o ! -d ${PCMCIA_SRC_DIR} ]; then
	echo "This package requires kernel and pcmcis-cs source."
	echo "For the kernel, run './ltib -m config' and enable the option"
	echo "'Leave the sources after building' and for pcmcia-cs,"
	echo "build the package and leave the source with:"
	echo "'./ltib -p pcmcia-cs -l'."
	exit 1
fi
BUILD_ROOT=$RPM_BUILD_ROOT/%{pfx}

cat <<HERE > $PRJ_BASE/tmp/wlan.config
PRISM2_PCMCIA=y
PRISM2_PLX=n
PRISM2_PCI=n
PRISM2_USB=n
LINUX_SRC=$KERNEL_SRC_DIR
PCMCIA_SRC=$PCMCIA_SRC_DIR
WLAN_KERN_PCMCIA=n
PCMCIA_DIR=/etc/pcmcia
TARGET_ROOT_ON_HOST=$BUILD_ROOT
INST_EXEDIR="/sbin"
RC_DIR=/etc/rc.d
SYSV_INIT=n
HOST_COMPILE=""
WLAN_TARGET_ARCH=$GNUTARCH
CROSS_COMPILE_ENABLED=y
CROSS_COMPILE="$TOOLCHAIN_PREFIX"
WLAN_DEBUG=n
TARGET_INST_EXEDIR=$RPM_BUILD_ROOT
HERE

./Configure -d $PRJ_BASE/tmp/wlan.config
make auto_config

HOST_CC="$BUILDCC" HOST_LD="$BUILDLD" HOST_STRIP="$BUILDSTRIP" make all

%Install
rm -rf $RPM_BUILD_ROOT
BUILD_ROOT=$RPM_BUILD_ROOT/%{pfx} make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


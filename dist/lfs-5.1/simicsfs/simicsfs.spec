%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : simics filesystem portal module
Name            : simicsfs
Version         : 1.9
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Kumar Gala
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Notes:

You need to have a built unpacked kernel source tree available
via $RPM_BUILD_DIR/linux.

We build spoofed, so gcc == the cross compiler

You can override: KERNELDIR, ARCH by passing these on the make command line

%Prep
%setup
cp Makefile_2.6 Makefile

%Build
KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}
if grep -q 'CONFIG_PPC_MERGE=y' $KBOUT/.config
then
    LINTARCH=powerpc
fi
if [ ! -f $KBOUT/.config ]
then
    cat <<TXT
You need a built unpacked kernel source tree in:
$KBOUT
to build kernel modules
TXT
    exit 1
fi
make M=`pwd` -C $KBOUT ARCH=$LINTARCH

%Install
rm -rf $RPM_BUILD_ROOT

KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}

if [ -f $KBOUT/include/config/kernel.release ]
then
    KVER=`cat $KBOUT/include/config/kernel.release`
else
    KVER=`strings $DEV_IMAGE/boot/vmlinux | perl -n -e 'print($1), exit(0) if m,Linux version ([\S]+),'`
fi
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/misc/
cp *.ko $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/misc/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


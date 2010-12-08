%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : Hello World module test package
Name            : hello_mod
Version         : 1.2
Release         : 1
License         : Public Domain, not copyrighted
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Test
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

%Build
KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}
CFG_PATH="$KBOUT/.config"
if [ $LINTARCH = ppc -a -f $KSRC_DIR/arch/powerpc/Kconfig ]
then
    if ! grep -q PPC_MERGE $KSRC_DIR/arch/powerpc/Kconfig
    then
        LINTARCH=powerpc
    else
        if [ -n "$CFG_PATH" ]
        then
            if grep -q 'CONFIG_PPC_MERGE=y' $CFG_PATH
            then
                LINTARCH=powerpc
            fi
        else
            LINTARCH=powerpc
        fi
    fi
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
make KERNELDIR=$KBOUT ARCH=$LINTARCH

%Install
rm -rf $RPM_BUILD_ROOT

KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}

if [ -f $KBOUT/include/config/kernel.release ]
then
    KVER=`cat $KBOUT/include/config/kernel.release`
else
    KVER="`perl -e '$/ = ""; $_ = <>; m,VERSION\s*=\s*(\d)\s*PATCHLEVEL\s*=\s*(\d+)\s*SUBLEVEL\s*=\s*(\d+)\s*EXTRAVERSION[ \t]*=[ \t]*(\S*),m; print  "$1.$2.$3$4"' $KSRC_DIR/Makefile`"
fi
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/misc/
cp *.ko $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/modules/$KVER/misc/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


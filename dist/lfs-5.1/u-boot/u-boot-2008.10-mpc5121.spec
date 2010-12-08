%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Universal Bootloader firmware
Name            : u-boot
Version         : 2008.10
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/System
Source          : u-boot-%{version}.final.tar.bz2
Patch1          : u-boot-2008.10-ADS5121-01-ADS5121-Do-not-include-FSL-logo.patch
Patch2          : u-boot-2008.10-ADS5121-02-Freescale-NFC-NAND-driver.patch
Patch3          : u-boot-2008.10-ADS5121-03-MPC5121-Hibernate-to-ram-support.patch
Patch4          : u-boot-2008.10-ADS5121-04-Add-CW-debug-support.patch
Patch5          : u-boot-2008.10-ADS5121-05-ADS5121-add-diu_bmp_command.patch
Patch6          : u-boot-2008.10-ADS5121-06-add-self_jffs2-and-othbootargs-e.patch
Patch7		: u-boot-2008.10-ADS5121-07-run-flash_jffs2-default-bootcmd.patch
Patch8		: u-boot-2008.10-ADS5121-08-fix-rev2-silicon-pci-iopads.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Open source u-boot v2008.10 plus Freescale patches

%Prep
%setup -n u-boot-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%Build
if [ -z "$PKG_U_BOOT_CONFIG_TYPE" ]; then
    echo PKG_U_BOOT_CONFIG_TYPE is not set
    exit 1
fi
make distclean
make HOSTCC="$BUILDCC" CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_CONFIG_TYPE
make HOSTCC="$BUILDCC" HOSTSTRIP="$BUILDSTRIP" \
    CROSS_COMPILE=$TOOLCHAIN_PREFIX $PKG_U_BOOT_BUILD_ARGS

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
for i in u-boot.bin u-boot
do
    cp $i $RPM_BUILD_ROOT/%{pfx}/boot
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

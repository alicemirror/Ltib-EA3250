%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Generate module dependency file
Name            : modeps
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/lib/modules
if [ -f $DEV_IMAGE/boot/vmlinux ]
then 
    # generate modules.conf
    KERNEL_VER=`strings $DEV_IMAGE/boot/vmlinux | perl -n -e 'print($1), exit(0) if m,Linux version ([\S]+),'`
    if [ -n "$KERNEL_VER" ]
    then
        mkdir -p $RPM_BUILD_ROOT/%{pfx}/lib/modules/$KERNEL_VER
        depmod.pl -b $DEV_IMAGE/lib/modules/$KERNEL_VER -F $DEV_IMAGE/boot/System.map --stdout > $RPM_BUILD_ROOT/%{pfx}/lib/modules/$KERNEL_VER/modules.dep
    fi
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


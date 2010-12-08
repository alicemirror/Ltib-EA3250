%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : PCMCIA utilities
Name            : pcmciautils
Version         : 014
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make V=true UDEV=true STARTUP=false  all

%Install
rm -rf $RPM_BUILD_ROOT
make V=true UDEV=true STARTUP=false DESTDIR=$RPM_BUILD_ROOT/%{pfx} install 

# edit and install the rc startup script
install -d $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d

# Map the platform to the name of the socket driver,
# and specify rc script permissions.
#
# $SOCKDRV is used in the sed script below to change the
# name of the socket driver that is modprobe'd at init time
#
# Add additional platforms as needed.
#
case "$PLATFORM" in
    imx31ads)
        SOCKDRV=mx31ads-pcmcia
        ;;
esac
sed -e "s/DRIVER=yenta_socket/DRIVER=$SOCKDRV/" < doc/pcmcia-new.sh > \
    $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/pcmcia


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

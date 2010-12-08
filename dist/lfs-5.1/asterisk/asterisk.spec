%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Asterisk - Soft PBX
Name            : asterisk
Version         : 1.4.21.1
Release         : z
License         : GPL
Vendor          : Digium
Packager        : Vadim Lebedev
Group           : Applications/Communication
URL             : http://xxxx
Source          : %{name}-%{version}.tar.gz
Patch1          : asterisk-1.4.21.1-cross.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}

PKG_ASTERISK_PRECONFIG=${PKG_ASTERISK_PRECONFIG:-asterisk.menuselect.makeopts}
if [ -f "$PLATFORM_PATH/${PKG_ASTERISK_PRECONFIG}" ]
then
    cp $PLATFORM_PATH/$PKG_ASTERISK_PRECONFIG menuselect.makeopts
else
    if [ -f "$CONFIG_DIR/defaults/$PKG_ASTERISK_PRECONFIG" ]
    then
        cp "$CONFIG_DIR/defaults/$PKG_ASTERISK_PRECONFIG"  menuselect.makeopts
    fi
fi
if [ -n "$PKG_ASTERISK_WANT_CF" -o -n "$SCB_WANT_CF" ]
then
    make menuconfig HOST_CC="$BUILDCC"
    cp menuselect.makeopts $PLATFORM_PATH/$PKG_ASTERISK_PRECONFIG
fi

make HOST_CC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make install HOST_CC="$BUILDCC" DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

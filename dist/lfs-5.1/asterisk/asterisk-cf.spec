%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Asterisk - Soft PBX
Name            : asterisk
Version         : 1.4.23.rc3
Release         : 1
License         : GPL
Vendor          : Digium
Packager        : Vadim Lebedev
Group           : Applications/Communication
URL             : http://downloads.digium.com/pub/asterisk/asterisk-1.4.23-rc3.tar.gz
Source          : %{name}-%{version}.tar.gz
Patch1          : asterisk-1.4.23.rc3-cross.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
ORIG_PATH=$PATH
TONEZONE_DIR=$RPM_BUILD_DIR/zaptel
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --with-zaptel --with-tonezone 
export PATH=$UNSPOOF_PATH

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
    make menuconfig -j1 HOSTCC="$BUILDCC"
    cp menuselect.makeopts $PLATFORM_PATH/$PKG_ASTERISK_PRECONFIG
fi
$BUILDCC -o channels/gentone channels/gentone.c -lm
cd menuselect && CC="$BUILDCC" ./configure && make -j1
export PATH=$ORIG_PATH
make -j1 HOST_CC="$BUILDCC"

%Install
rm -rf $RPM_BUILD_ROOT
make install -j1 HOSTCC="$BUILDCC" DESTDIR=$RPM_BUILD_ROOT/%{pfx}
make samples -j1 HOSTCC="$BUILDCC" DESTDIR=$RPM_BUILD_ROOT/%{pfx}

if grep -q 'CONFIG_PKG_ASTERISK_GUI=y' $PLATFORM_PATH/.config
then 
cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/asterisk/http.conf
[general]
enabled = yes
enablestatic = yes
bindport = 8088
prefix = asterisk
EOF

cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/asterisk/manager.conf
[general]
enabled = yes
webenabled = yes

[admin]
secret = admin
read = system,call,log,verbose,command,agent,config
write = system,call,log,verbose,command,agent,config
EOF
fi

if grep -q 'CONFIG_PLATFORM="m54451evb"' $PLATFORM_PATH/.config
then 
cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/asterisk/zapata.conf
[trunkgroups]

[channels]
context = default
switchtype = national
signalling = fxo_ls
rxwink = 300
usecallerid = yes
hidecallerid = no
callwaiting = yes
usecallingpres = yes
callwaitingcallerid = yes
threewaycalling = yes
transfer = yes
canpark = yes
cancallforward = yes
callreturn = yes
echocancel = no
echocancelwhenbridged = yes
rxgain = 0.0
txgain = 0.0
group = 1
callgroup = 1
pickupgroup = 1
immediate = no

signalling=fxs_ks
context=DID_trunk_1
group = 2
channel => 2
 
signalling=fxo_ks
group = 1
context=default
context=DLPN_DialPlan1
channel => 1
EOF

#This is the script to start asterisk
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/
cat <<EOF > $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/asteriskd
#!/bin/sh

modprobe mcf_wcfxs
ztcfg
asterisk
EOF

chmod a+x $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d/asteriskd
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

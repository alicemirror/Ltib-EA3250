%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Internet Systems Consortium DHCP server, client, and relay agent
Name            : dhcp
Version         : 3.0.3b1
Release         : 1
License         : Internet Systems Consortium (distributable)
Vendor          : Freescale
Packager        : John Faith
Group           : Applications/Internet
Source          : dhcp-3.0.3b1.tgz
Patch1          : dhcp-3.0.3b1-sip.patch
Patch2          : dhcp-3.0.3b1-defaults.patch
Patch3          : dhcp-3.0.3b1-types.patch
Patch4          : dhcp-3.0.3b1-usesockets.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://www.isc.org/sw/dhcp/

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
./configure
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share
mv $RPM_BUILD_ROOT/%{pfx}/usr/man  $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share
chmod 755 $RPM_BUILD_ROOT/%{pfx}/%base/sbin/dhclient-script

for i in %pfx/%base/etc/test %pfx/%base/etc/rc.d \
         %pfx/%base/sbin/S30dhclient %pfx/%_prefix/local
do
    rm -rf $RPM_BUILD_ROOT/$i
done

if [ -z "$PKG_DHCP_WANT_CLIENT" ]
then
    for i in %pfx/%base/etc/dhclient.conf \
             %pfx/%base/var/state/dhcp/dhclient.leases \
             %pfx/%base/sbin/dhclient-script \
             %pfx/%base/sbin/dhclient \
             %pfx/%base/bin/parse \
             %pfx/%base/etc/dhclient-exit-hooks \
             %pfx/%base/etc/dhclient.conf \
             %pfx/%_mandir/man5/dhclient.conf.5 \
             %pfx/%_mandir/man5/dhclient.leases.5 \
             %pfx/%_mandir/man8/dhclient-script.8 \
             %pfx/%_mandir/man8/dhclient.8
    do
        rm -rf $RPM_BUILD_ROOT/$i
    done
fi
if [ -z "$PKG_DHCP_WANT_SERVER" ]
then
    for i in %pfx/%base/etc/dhcpd.conf \
             %pfx/%_bindir/omshell \
             %pfx/%_mandir/man1/omshell.1 \
             %pfx/%_mandir/man3/dhcpctl.3 \
             %pfx/%_mandir/man3/omapi.3 \
             %pfx/%_mandir/man3/omshell.3 \
             %pfx/%_mandir/man5/dhcp-eval.5 \
             %pfx/%_mandir/man5/dhcp-options.5 \
             %pfx/%_mandir/man5/dhcpd.conf.5 \
             %pfx/%_mandir/man5/dhcpd.leases.5 \
             %pfx/%_mandir/man8/dhcpd.8 \
             %pfx/%_mandir/man8/dhcrelay.8 \
             %pfx/%_sbindir/dhcpd \
             %pfx/%_sbindir/dhcrelay \
             %pfx/%base/var/state/dhcp/dhcpd.leases
     do
        rm -rf $RPM_BUILD_ROOT/$i
     done
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


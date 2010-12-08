%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Boot Time Critical Services
Name            : btcs
Version         : 1.2.1
Release         : 0
License         : BSD and GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Device Drivers
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
if [ -z "$PKG_BTCS_WANT_SERVICES$PKG_BTCS_WANT_TESTAPP" ]; then
    PKG_BTCS_WANT_TESTAPP=y
fi

if [ -n "$PKG_BTCS_WANT_SERVICES" ]; then
    make btcs_cb btcs_app btcs_isr
fi

if [ -n "$PKG_BTCS_WANT_TESTAPP" ]; then
    make btcs_test
fi

%Install
if [ -z "$PKG_BTCS_WANT_SERVICES$PKG_BTCS_WANT_TESTAPP" ]; then
    PKG_BTCS_WANT_TESTAPP=y
fi

if [ -n "$PKG_BTCS_WANT_SERVICES" ]; then
    install -d $RPM_BUILD_ROOT/%{pfx}/usr/bin
    cp -a btcs_app/btcs_app $RPM_BUILD_ROOT/%{pfx}/usr/bin
    install -d $RPM_BUILD_ROOT/%{pfx}/boot/btcs
    cp -a btcs_isr/btcs_isr  $RPM_BUILD_ROOT/%{pfx}/boot/btcs
    cp -a btcs_isr/btcs_isr.bin  $RPM_BUILD_ROOT/%{pfx}/boot/btcs
    cp -a btcs_cb/btcs_cb  $RPM_BUILD_ROOT/%{pfx}/boot/btcs
    cp -a btcs_cb/btcs_cb.bin  $RPM_BUILD_ROOT/%{pfx}/boot/btcs
fi

if [ -n "$PKG_BTCS_WANT_TESTAPP" ]; then
    install -d $RPM_BUILD_ROOT/%{pfx}/usr/bin
    cp -a btcs_test/btcs_test $RPM_BUILD_ROOT/%{pfx}/usr/bin
    cp -a btcs_test/pcanflood $RPM_BUILD_ROOT/%{pfx}/usr/bin
fi

%Clean
make clean

%Files
%defattr(-,root,root)
%{pfx}/*

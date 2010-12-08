%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Peak Linux CAN driver
Name            : peak-linux-driver
Version         : 3.17
Release         : 1
License         : GPL
Vendor          : Peak Systems + Freescale patch
Packager        : John Rigby
Group           : System Environment/Libraries
URL             : http://www.peak-system.com/linux
Source          : %{name}.%{version}.tar.gz
Patch0          : %{name}-%{version}-mpc5200.patch
Patch1          : %{name}-%{version}-mpc5200-platform_driver.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1

%Build
make KERNEL_LOCATION=$TOP/rpm/BUILD/linux-2.6.16 KERNSRC=$TOP/rpm/BUILD/linux-2.6.16 CROSS_COMPILE=$TOOLCHAIN_PREFIX ARCH=ppc


%Install
install -d $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp test/bitratetest $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp test/transmitest $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp test/receivetest $RPM_BUILD_ROOT/%{pfx}/usr/bin
install -d $RPM_BUILD_ROOT/%{pfx}/usr/lib
cp -a lib/libpcan.so* $RPM_BUILD_ROOT/%{pfx}/usr/lib
install -d $RPM_BUILD_ROOT/%{pfx}/usr/lib/can
cp test/transmit.txt $RPM_BUILD_ROOT/%{pfx}/usr/lib/can
install -d $RPM_BUILD_ROOT/%{pfx}/lib/modules/2.6.16/can
cp driver/pcan.ko $RPM_BUILD_ROOT/%{pfx}/lib/modules/2.6.16/can


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

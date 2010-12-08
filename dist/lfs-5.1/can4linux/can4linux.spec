%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Linux CAN/CANopen driver
Name            : can4linux
Version         : 3.3.3
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
URL             : http://www.port.de/engl/canprod/content/linux_e.html
Source          : %{name}.%{version}.tgz
Patch1          : can4linux-mmuless.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n can4linux-examples
%patch1 -p1

%Build
make CFLAGS="-Wall -I../can4linux-3.3.3"

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/bin
# possible list is: ctest baud can_send acceptance noiser receive transmit \
#                   can_verify receive-select transmit-select
for i in ctest can_send receive
do
    cp $i $RPM_BUILD_ROOT/%{pfx}/bin/$i
done


%Clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/can4linux-*

%Files
%defattr(-,root,root)
%{pfx}/*

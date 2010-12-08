%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : i2c tools
Name            : i2c-tools
Version         : 3.0.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
URL             : http://www.lm-sensors.org/wiki/I2CTools
Source          : i2c-tools-3.0.2.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
for i in i2cdetect i2cset i2cget i2cdump
do
    cp -a tools/$i $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/$i
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : User space application and ip layer7 filter for PME 
Name            : fsl_pme
Version         : 1.0.0
Release         : alpha5
License         : Freescale EULA
Vendor          : Freescale
Packager        : Haiying Wang
Group           : Development/Debuggers
Source          : %{name}-%{version}-%{release}-3.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make SYS_PATH=$TOP/rootfs/usr/ KERNEL_SRC=$TOP/rpm/BUILD/linux-2.6.23 KERNEL_VER=2.6.23

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/sbin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/%{pfx}/fsl_pme/
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc/l7-protocols/
cp fsl_pme/pme_dev_init $RPM_BUILD_ROOT/%{pfx}/etc/rc.d/init.d
cp fsl_pme/bin/* $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin/
cp fsl_pme/hotplug $RPM_BUILD_ROOT/%{pfx}/sbin/
cp fsl_pme/sample* $RPM_BUILD_ROOT/%{pfx}/fsl_pme/
cp fsl_ipt_l7pm/*.ko $RPM_BUILD_ROOT/%{pfx}/etc/l7-protocols/
cp fsl_ipt_l7pm/layer7.* $RPM_BUILD_ROOT/%{pfx}/etc/l7-protocols/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

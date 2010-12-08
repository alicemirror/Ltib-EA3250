%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNU version of the tar archiving utility
Name            : spi-test
Version         : 0.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Ebony Zhu
Group           : Applications
Source          : %{name}-%{version}.tgz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
make CROSS_COMPILE=$TOOLCHAIN_PREFIX

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/tmp
cp test_83xx_spi_rev21 $RPM_BUILD_ROOT/%{pfx}/tmp

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Advanced Java-based cellphone environment
Name            : phoneme_advanced-mr2
Version         : rev1427
Release         : 20070131
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
URL             : https://phoneme.dev.java.net/
Source          : %{name}-%{version}.zip
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}

%Build
cd build/linux-arm-mx31
make clean
make bin \
          BINARY_BUNDLE_DIRNAME=phoneme_adv \
#         BINARY_BUNDLE_APPEND_REVISION=false

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
unzip -d $RPM_BUILD_ROOT/%{pfx} install/*.zip

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}
%define codec_package axe_codec_binaries-3.1-1.tar.gz
%define scheduler_package axe_scheduler_bin_22Feb2008.tgz

Summary         : AXE binaries for mpc5121
Name            : axe_binaries
Version         : 1.0
Release         : 1
License         : Freescale EULA
Vendor          : Freescale
Packager        : John Rigby
Group           : Drivers/Sound
Source1		: %{codec_package}
Source2		: %{scheduler_package}
BuildRoot       : %{_tmppath}/axe
Prefix          : %{pfx}

%Description
%{summary}

%Prep

%Build

%Install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/usr/lib
cd $RPM_BUILD_ROOT/%{pfx}/%{base}/usr/
tar xvzf ${RPM_SOURCE_DIR}/%{scheduler_package} \
    --transform='s,axe_lib,lib,' --show-transformed-names
tar xvzf ${RPM_SOURCE_DIR}/%{codec_package} \
    --transform='s,axe_lib,lib,' --show-transformed-names

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


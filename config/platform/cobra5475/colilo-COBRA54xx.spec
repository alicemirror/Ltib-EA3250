%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : COldfire LInux boot LOader
Name            : colilo
Version         : 0.3.3
Release         : 2
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}-fsl.tar.gz
Patch1		    : colilo_cache.patch
Patch2          : colilo-gcc-4.1.patch
Patch3          : colilo-COBRA54xx.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n colilo
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
make clean
make VENDOR=senTec BOARD=cobra5475 CONFIG_FLASH=1 CONFIG_COLILO_SOLO=1 ARCH=5475
cp -f colilo.bin colilo_mcf5475.bin
cp -f colilo.srec colilo_mcf5475.srec

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
for i in colilo_mcf5475.srec colilo_mcf5475.bin
do
   cp -a $i $RPM_BUILD_ROOT/%{pfx}/boot
done
                            

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

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
Patch1		: colilo_cache.1.patch
Patch2          : colilo-gcc-4.1.patch
Patch3          : colilo-reloc.patch
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
make BOARD=FireEngine CONFIG_FLASH=1 ARCH=5485
cp -f colilo.srec colilo_mcf5485_flash.srec
cp -f colilo.elf colilo_mcf5485_flash.elf
make clean
make BOARD=FireEngine CONFIG_FLASH=1 CONFIG_COLILO_SOLO=1 ARCH=5485
cp -f colilo.elf colilo_mcf5485_only.elf
cp -f colilo.bin colilo_mcf5485_only.bin
make clean
make BOARD=FireEngine CONFIG_FLASH=0 ARCH=5485
cp -f colilo.srec colilo_mcf5485.srec
cp -f colilo.elf colilo_mcf5485.elf
make clean
make BOARD=FireEngine CONFIG_FLASH=1 ARCH=5475
cp -f colilo.srec colilo_mcf5475_flash.srec
cp -f colilo.elf colilo_mcf5475_flash.elf
make clean
make BOARD=FireEngine CONFIG_FLASH=1 CONFIG_COLILO_SOLO=1 ARCH=5475
cp -f colilo.elf colilo_mcf5475_only.elf
cp -f colilo.bin colilo_mcf5475_only.bin
make clean
make BOARD=FireEngine CONFIG_FLASH=0 ARCH=5475
cp -f colilo.srec colilo_mcf5475.srec
cp -f colilo.elf colilo_mcf5475.elf

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/boot
for i in colilo_mcf5485.srec         colilo_mcf5485_only.bin \
         colilo_mcf5485_flash.srec   colilo_mcf5475.srec     \
         colilo_mcf5475_only.bin     colilo_mcf5475_flash.srec
do
    cp -a $i $RPM_BUILD_ROOT/%{pfx}/boot
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

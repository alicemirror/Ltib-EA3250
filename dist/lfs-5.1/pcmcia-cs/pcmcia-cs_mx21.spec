%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : PCMCIA utilities
Name            : pcmcia-cs
Version         : 3.2.4
Release         : 1
License         : Mozilla Public License Version 1.1
Vendor          : Freescale
Packager        : John Faith
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
Patch0          : pcmcia-cs-3.2.4-mx21.patch
Patch1          : pcmcia-cs-3.2.4-mx21-sysconfig.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1

%Build
./Configure \
	--target=$RPM_BUILD_ROOT/%{pfx} \
	--arch=%{_target_cpu} \
	--kflags="-Wall -Wstrict-prototypes -O2  -fno-strict-aliasing -fno-common -pipe -fno-omit-frame-pointer -mapcs-32 -march=armv5 -mtune=arm9tdmi -mshort-load-bytes -msoft-float" \
	--srctree \
	--kernel=${RPM_BUILD_DIR}/linux \
	--sysv \
	--rcdir=/etc/rc.d \
	--apm \
	--notrust \
	--nocardbus \
	--noprompt \
	--nopnp

# Allow 'make install' to overwrite man pages
chmod u+w man/*.[1458]

make all

%Install
make install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


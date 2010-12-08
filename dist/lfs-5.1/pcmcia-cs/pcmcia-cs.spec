%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : PCMCIA utilities
Name            : pcmcia-cs
Version         : 3.2.8
Release         : 1
License         : MPL/GPL
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
chmod +x Configure.ltib
./Configure.ltib \
    --noprompt \
	--arch=%{_target_cpu} \
	--target=$RPM_BUILD_ROOT/%{pfx} \
	--sysv --rcdir=/etc/rc.d \
	--notrust --nocardbus --nox11
make all

%Install
make install

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

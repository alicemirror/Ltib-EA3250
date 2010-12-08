%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : TCP/IP swiss army knife
Name            : netcat
Version         : 1.10
Release         : 1
License         : Public domain
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Internet
URL             : http://download.insecure.org/stf/nc110.tgz
Source          : nc110.tgz
Patch1          : netcat-1.10-res_init.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

See: http://sectools.org/netcats.html

%Prep
%setup -c
%patch1 -p1


%Build
make linux STATIC=

%Install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
install -m 755 nc $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

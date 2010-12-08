%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : devfs userspace daemon
Name            : devfsd
Version         : 1.3.25
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Daemons
Source          : %{name}-v%{version}.tar.gz
Patch0          : devfsd-uclibc-nls.patch
Patch1          : devfsd-1.3.25-devfs_fs-hdr.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}
%patch0 -p1
%patch1 -p1

%Build
make KERNEL_DIR=$DEV_IMAGE/usr WITHOUT_NSL=1

%Install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}  

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

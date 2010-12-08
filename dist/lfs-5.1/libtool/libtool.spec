%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNU libtool, shared libraries management tool.
Name            : libtool
Version         : 1.5
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
if [ -n "$DEFPFX" -a "$DEV_IMAGE" = "$DEFPFX" ]
then
    INST_PREFIX=$DEFPFX
fi
./configure --prefix=$INST_PREFIX/%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



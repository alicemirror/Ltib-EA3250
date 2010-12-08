%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A GNU tool for automatically configuring source code
Name            : autoconf
Version         : 2.57
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : autoconf-2.57.tar.bz2
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
./configure --prefix=$INST_PREFIX/%{_prefix} mandir='${prefix}/share/man'
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



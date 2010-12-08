%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A document formatting system
Name            : groff
Version         : 1.18.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : groff-1.18.1.tar.gz
Patch0          : groff-1.18.1-crossbuild.patch
Patch1          : groff-post-html.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p0

%Build
PAGE=A4 ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir='${prefix}/share/man'
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make -j1 install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
ln -s soelim $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/zsoelim
ln -s eqn $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/geqn
ln -s tbl $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/gtbl

%Clean
rm -rf $RPM_BUILD_ROOT

rm -f /tmp/groff-*

%Files
%defattr(-,root,root)
%{pfx}/*



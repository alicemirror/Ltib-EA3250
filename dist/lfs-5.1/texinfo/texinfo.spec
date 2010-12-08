%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Tools needed to create Texinfo format documentation files.
Name            : texinfo
Version         : 4.8
Release         : 2
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes, Steve Papacharalambous
Group           : Applications/Publishing
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
#BuildRequires   : ncurses

%Description
%{summary}

%Prep
%setup

%Build
export BUILD_CC="$BUILDCC"
export BUILD_AR="/usr/bin/ar"
export BUILD_RANLIB="/usr/bin/ranlib"
# this is to avoid a compiler bug (any -O except 0 causes internal compiler err)
if [ "$PLATFORM" = "mcf547x_8x" ]
then
  CFLAGS="-g" ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
else
              ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



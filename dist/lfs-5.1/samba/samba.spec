%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Samba is useful for creating and connecting to Windows shares using the SMB protocol
Name            : samba
Version         : 3.0.32
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Michael Reiss
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch1          : samba-3.0.32-linux-setlease-fix.patch
Patch2          : samba-3.0.32-cross-configure-workaround.patch
Patch3          : samba-3.0.32-add-site-files.patch
Patch4          : samba-3.0.32-for-uclinux1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
cd source
if [ ${CPU} = "MPC8315E" ] || [ ${CPU} = "MPC837xE" ] ; then
echo "***** Using CPU specific .site file for cross building settings *****"
CONFIG_SITE=samba-3.0.32-mpc8315-mpc837x.site ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --target=$CFGHOST --with-sendfile-support --disable-cups
else
if [ "$GNUTARCH" = m68knommu ]; then
echo "***** Using mmuless specific .site file for cross building settings *****"
CONFIG_SITE=samba-3.0.32-cf-nommu.site ./configure --prefix=/ --host=$CFGHOST --build=%{_build} --target=$CFGHOST --with-sendfile-support --disable-cups --with-privatedir=/tmp
else
echo "***** Using default site file for cross build settings *****"
CONFIG_SITE=samba-3.0.32-default.site ./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --target=$CFGHOST --with-sendfile-support --disable-cups
fi
fi
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
cd source
# make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
if [ "$GNUTARCH" = m68knommu ]; then
# samba servers do not work without a valid fork() call.
make installbin DESTDIR=$RPM_BUILD_ROOT/%{pfx}
else
make installservers installbin DESTDIR=$RPM_BUILD_ROOT/%{pfx}
fi

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

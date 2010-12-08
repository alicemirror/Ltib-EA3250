%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : X.Org X11 libXt runtime library
Name            : libXt
Version         : 1.0.4
Release         : 5
License         : MIT
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : System Environment/Libraries
URL             : http://www.x.org
Source0         : ftp://ftp.x.org/pub/individual/lib/libXt-1.0.4.tar.bz2
Patch0          : libXt-1.0.2-libsm-fix.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms libXt-1.0.4-5.fc9.src.rpm

%Prep

%setup -q


%Build
# FIXME: Work around pointer aliasing warnings from compiler for now
export CFLAGS="-fno-strict-aliasing"
./configure \
  --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
  --disable-malloc0returnsnull \
  --disable-static \
  --disable-install-makestrs \
  --with-xfile-search-path="%{_sysconfdir}/X11/%%L/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%l/%%T/\%%N%%C%%S:%{_sysconfdir}/X11/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%L/%%T/%%N%%S:%{_sysconfdir}/X\11/%%l/%%T/%%N%%S:%{_sysconfdir}/X11/%%T/%%N%%S:%{_datadir}/X11/%%L/%%T/%%N%%C%%S:%{_datadir}/X1\1/%%l/%%T/%%N%%C%%S:%{_datadir}/X11/%%T/%%N%%C%%S:%{_datadir}/X11/%%L/%%T/%%N%%S:%{_datadir}/X11/%%\l/%%T/%%N%%S:%{_datadir}/X11/%%T/%%N%%S"

perl -pi.bak -e 's,^CC = gcc,CC = $ENV{BUILDCC},;
                 s,$ENV{DEV_IMAGE}/usr/include,/usr/include,g;
            ' util/Makefile

make HOSTCC="$BUILDCC"


%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

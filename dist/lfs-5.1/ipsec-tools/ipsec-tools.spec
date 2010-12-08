%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Userspace IPsec tools for the Linux IPsec implementation
Name            : ipsec-tools
Version         : 0.7.1
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : %{name}-%{version}.tar.gz
Patch1          : ipsec-tools-0.6.4-glob_tilde.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1 

%Build
export X_DIR=`echo $TOOLCHAIN_PREFIX | sed -e 's,-$,,'`
export TC_PREFIX="`which ${TOOLCHAIN_PREFIX}gcc | perl -p -e 's,/bin/'${TOOLCHAIN_PREFIX}'gcc,,'`"
KHDR=`perl -e '
    foreach $path ("$ENV{TC_PREFIX}/$ENV{X_DIR}/include/linux/version.h",
                   "$ENV{TC_PREFIX}/include/linux/version.h",
                   "$ENV{TC_PREFIX}/$ENV{X_DIR}/sysroot/usr/include/linux/version.h",
                   "$ENV{TC_PREFIX}/$ENV{X_DIR}/libc/usr/include/linux/version.h") {
        if(-f $path) {
            warn "found $path";
            $path = @ARGV = ($path);
            last;
        }
    }
    warn("Cannot find version.h\n"), exit(1) unless @ARGV;
    $path = $ARGV[0];
    while(<>) {
        m,UTS_RELEASE\s+"2\.(\d), && do { $lin_series = $1; last };
    }
    if($lin_series eq "4") { 
        print "$ENV{DEV_IMAGE}/usr/src/linux/include";
    } else {
        $path =~ s,/linux/version.h,,;
        print $path;
    }
    exit(0);
    '`

CFLAGS="-isystem ${TC_PREFIX}/${X_DIR}/include" \
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} \
            --host=$CFGHOST --build=%{_build} \
            --with-kernel-headers=$KHDR \
            --mandir=%{_mandir} \
            --enable-security-context=no

# Remove -Werror from the CFLAGS as this causes a build failure with gcc-4.2.x
# Stevep - 14jan08
perl -pi.orig -e 's,(^CFLAGS_ADD=.*)\s+\-Werror(.*),$1$2,' configure

make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

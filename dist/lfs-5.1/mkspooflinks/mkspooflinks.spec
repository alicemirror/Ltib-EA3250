%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Setup for compiler spoofing (needed for interface lib/hdrs)
Name            : mkspooflinks
Version         : 3.4
Release         : 4
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
Source          : %{name}-%{version}.tar.gz
Patch1          : mkspooflinks-3.4-mmlink.patch
Patch2          : mkspooflinks-3.4-prefixbefore.patch
Patch3          : mkspooflinks-3.4-ccache.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1


%Build
CROSSGCC=gcc
if [ "$TOOLCHAIN_PATH" != "" ]
then
    CROSSGCC=$TOOLCHAIN_PATH/bin/${TOOLCHAIN_PREFIX}gcc
fi
LIBGCC_A="`$CROSSGCC -print-libgcc-file-name`"
LIBGCC_DIR="`dirname $LIBGCC_A`"
GCC_VERSION="`$CROSSGCC -dumpversion`"

export CFLAGS="-DLTIB_BUILD -D__UCLIBC_CTOR_DTOR__ -D__UCLIBC_HAS_SHARED__ -DLIBGCC_DIR=\"$LIBGCC_DIR\" -DGCC_VERSION=\"$GCC_VERSION\""
cd extra/gcc-uClibc
gcc -O2 -g $CFLAGS gcc-uClibc.c -o tc_wrapper


%Install
rm -rf $RPM_BUILD_ROOT
sh mkspoof $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/spoof/
cp extra/gcc-uClibc/tc_wrapper $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/spoof/


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


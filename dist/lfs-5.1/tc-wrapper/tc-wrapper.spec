%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}


Summary         : Toolchain isolation wrapper
Name            : tc-wrapper
Version         : 0.1
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
Patch1          : tc-wrapper-0.1-tc_cflags-2.patch
Patch2          : tc-wrapper-0.1-cache_libgcc_dir-1.patch
Patch3          : tc-wrapper-0.1-cplusplus.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This wrapper was originally from uClibc but was obsoleted as it is
imperfect and has been superceeded by native uClibc toolchains.
However this still has utility in some situations when doing
initial ports and you only have a toolchain build around a different
library available:

NOTE: this package builds a host side utility that is built per
project (at the moment).  There are no files in the target rpm.

%Prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1

%Build
CROSSGCC=$TOOLCHAIN_PATH/bin/${TOOLCHAIN_PREFIX}gcc
LIBGCC_A="`$CROSSGCC -print-libgcc-file-name`"
LIBGCC_DIR="`dirname $LIBGCC_A`"
GCC_VERSION="`$CROSSGCC -dumpversion`"

export CFLAGS="-DLTIB_BUILD -D__UCLIBC_CTOR_DTOR__ -DLIBGCC_DIR=\"$LIBGCC_DIR\" -DGCC_VERSION=\"$GCC_VERSION\""
if [ -n "$SYS_WANT_MMU" ]
then
    export CFLAGS="$CFLAGS -D__UCLIBC_HAS_MMU__"
fi
if [ -n "$SYS_WANT_SHARED" ]
then
    export CFLAGS="$CFLAGS -D__UCLIBC_HAS_SHARED__"
fi
cd extra/gcc-uClibc
$BUILDCC $CFLAGS gcc-uClibc.c -o tc-uclibc-gcc

%Install
rm -rf $RPM_BUILD_ROOT
if [ -n "$TOP" ]
then
    for i in gcc cc g++ c++
    do
        rm -f $TOP/bin/$i
    done
    cp extra/gcc-uClibc/tc-uclibc-gcc $TOP/bin/gcc
    ln -s gcc $TOP/bin/cc
    ln -s gcc $TOP/bin/g++
    ln -s gcc $TOP/bin/c++
fi


%Postun
if [ -n "$TOP" ]
then
    echo "removing $TOP/bin/{gcc,cc}"
    rm -f $TOP/bin/{gcc,cc}
fi


%Clean
rm -rf $RPM_BUILD_ROOT

#%Files
#%defattr(-,root,root)

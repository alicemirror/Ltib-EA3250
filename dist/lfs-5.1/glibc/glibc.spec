%define pfx /opt/freescale/rootfs/%{_target_cpu} 
%define cs_version 4.2-187

Summary         : GNU standard C library with NPTL thread library.
Name            : glibc
Version         : 2.5
Release         : 2
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes & Steve Papacharalambous
Group           : System Environment/Libraries
Source0         : %{name}-%{version}.tar.bz2
Source1         : %{name}-ports-%{version}.tar.bz2
Source2         : %{name}-libidn-%{version}.tar.bz2
Patch0		: %{name}-%{cs_version}-from-fsf-2_5.diff.gz
Patch1		: %{name}_ports-%{cs_version}-from-fsf-2_5.diff.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This glibc package is built using glibc-2.5 and glibc-ports-2.5 plus the
following patches from the CodeSourcery %{cs_version} release:

- glibc-4.2-187-from-fsf-2_5.diff
- glibc_ports-4.2-187-from-fsf-2_5.diff

The glibc and glibc-ports tarballs can be obtained from any of the GNU ftp
sites or their mirrors.
The CodeSourcery patch can be obtained by downloading the source rpm:
freescale-powerpc-linux-gnu-%{cs_version}.src.rpm from:
http://www.codesourcery.com/gnu_toolchains/power/download.html and then
extracting the glibc and glibc-ports patchs from this source rpm.


%Prep
%setup 
%patch0 -p1
tar jxvf %{SOURCE1}
cd glibc-ports-%{version}
%patch1 -p1
cd ..
ln -s glibc-ports-%{version} ports
tar jxvf %{SOURCE2}
ln -s glibc-libidn-%{version} libidn


%Build
# Temporary hack - stevep
# For building toolchain components an optimized version of the
# target is needed.  This should really be defined in the config
# area of ltib, and not done in the toolchain spec files.
# For now we assume that the optimised target can be derived by
# stripping the trailing "-" off the toolchain prefix, but this
# will not be true for all cases, eg when using uClibc toolchains.
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`

# Use the toolchain headers as the default for the glibc build unless the
# BSP kernel headers have been selected.
if [ "${GLIBC_WANT_KERNEL_HEADERS}" = "y" ]
then
    TC_HEADERS_DIR="${DEV_IMAGE}/usr/src/linux/include"
else
    TC_HEADERS_DIR="${TOOLCHAIN_PATH}/${OPT_CFGHOST}/libc/usr/include"
fi

# Add platform specific configuration options.
if [ "${SOFT_FP_ARCH}" = "y" ]
then
    ARCH_GLIBC_CONFIG="--without-fp"
else
    ARCH_GLIBC_CONFIG=""
fi


rm -rf build-glibc
mkdir build-glibc
cd build-glibc
BUILD_CC="${BUILDCC}" \
CFLAGS="-O2 ${TOOLCHAIN_CFLAGS}" \
../configure \
  --prefix=/usr \
  --build=%{_build} \
  --host=${OPT_CFGHOST} \
  --disable-profile \
  --without-gd \
  --without-cvs \
  --enable-kernel=2.6.10 \
  --with-headers=${TC_HEADERS_DIR} \
  --enable-add-ons=ports,nptl,libidn ${ARCH_GLIBC_CONFIG}
make

%Install
cd build-glibc
make install install_root=${RPM_BUILD_ROOT}/%{pfx}

# remove absolute paths from text search files (if they exist)
perl -w -e '
    @ARGV = grep { `file $_` =~ m,ASCII C program text, } @ARGV;
    exit(0) unless @ARGV;
    $^I = ".bak";
    while(<>) {
        s,[\S/]+/,,g if m,^GROUP,;
        print;
    }
    ' ${RPM_BUILD_ROOT}/%{pfx}/lib/libc.so \
      ${RPM_BUILD_ROOT}/%{pfx}/lib/libpthread.so \
      ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/lib/libc.so \
      ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/lib/libpthread.so

# Remove libtool .la files.
find $RPM_BUILD_ROOT/%{pfx} -name \*.la -exec rm {} \;


%Clean
rm -rf ${RPM_BUILD_ROOT}


%Files
%defattr(-,root,root)
%{pfx}/*



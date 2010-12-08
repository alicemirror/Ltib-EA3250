%define pfx /opt/freescale/rootfs/%{_target_cpu} 
%define linux_san_hdr_ver linux-libc-headers-2.6.11.2

Summary         : Gnu standard C library with linuxthreads
Name            : glibc
Version         : 2.3.2
Release         : 1
License         : LGPL
Vendor          : Freescale
Packager        : Stuart Hughes & Steve Papacharalambous
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.bz2
Source1         : %{name}-linuxthreads-%{version}.tar.bz2
Source2         : %{linux_san_hdr_ver}.tar.bz2
Patch0		: arm-asm-clobber.patch
Patch1		: arm-ctl_bus_isa.patch
Patch2		: arm-mcount_internal.patch
Patch3		: epoll-epollet.patch
Patch4		: epoll-stdint.patch
Patch5		: errlist-awk.patch
Patch6		: fixup.patch
Patch7		: gcc-pr-9552-workaround.patch
Patch8		: glibc-2.2.5-crosstest.patch
Patch9		: glibc-2.2.5-mips-clone-local-label.patch
Patch10		: glibc-2.3.2-allow-gcc-3.4-inline.patch
Patch11		: glibc-2.3.2-allow-gcc-3.4-nounit.patch
Patch12		: glibc-2.3.2-allow-gcc-3.5-elf.patch
Patch13		: glibc-2.3.2-allow-gcc-3.5-gconv.patch
Patch14		: glibc-2.3.2-allow-gcc-3.5-msort.patch
Patch15		: glibc-2.3.2-allow-gcc-3.5-PR14096.patch
Patch16		: glibc-2.3.2-allow-gcc-3.5-sunrpc.patch
Patch17		: glibc-2.3.2-allow-gcc-3.5-xdr.patch
Patch18		: glibc-2.3.2-alpha-pwrite64.patch
Patch19		: glibc-2.3.2-arm-fix-strlen.patch
Patch20		: glibc-2.3.2-cross-2.patch
Patch21		: glibc-2.3.2-cross.patch
Patch22		: glibc-2.3.2-cygwin.patch
Patch23		: glibc-2.3.2-mips.patch
Patch24		: glibc-2.3.2-mips-user.patch
Patch25		: glibc-2.3.2-override.patch
Patch26		: glibc-2.3.2-powerpc-as.patch
Patch27		: glibc-2.3.2-powerpc-procfs.patch
Patch28		: glibc-2.3.2-pr139-fix.patch
Patch29		: glibc-2.3.2-sh4-socket.patch
Patch30		: glibc-2.3.2-sh4-trapa.patch
Patch31		: glibc-2.3.2-sparc32-sysdep.patch
Patch32		: glibc-2.3.2-sparc64-dl-machine.patch
Patch33		: glibc-2.3.2-sparc64-pause.patch
Patch34		: glibc-2.3.2-sparc64-pwrite64.patch
Patch35		: glibc-2.3.2-without-fp.patch
Patch36		: glibc-configure-apple-as.patch
Patch37		: glibc-drow-sh.patch
Patch38		: glibc-fp-byteorder.patch
Patch39		: glibc-test-lowram.patch
Patch40		: nobits.patch
Patch41		: sscanf.patch
Patch42		: string2-typedef.patch
Patch43		: alpha_cfi1.patch
Patch44		: alpha_cfi2.patch
Patch45		: glibc-2.3.2-sparc64-sigproc.patch
Patch46		: glibc-linuxthreads-2.3.2-allow-3.4.patch
Patch47		: glibc-linuxthreads-2.3.2-cygwin.patch
Patch48		: sysdep-cancel-arm-1.2-1.6.patch
Patch49		: glibc-2.3.2-spe-ltib.patch.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
cd ${RPM_BUILD_DIR}/%{name}-%{version}
tar jxvf %{SOURCE1}
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1

# Add the spe patches for e500 builds.
if [ `echo ${TOOLCHAIN_PREFIX} | grep "gnuspe"` ]
then
%patch49 -p1
fi
cd ..
rm -rf %{linux_san_hdr_ver} 
tar --bzip2 -xvf %{SOURCE2}
cd %{linux_san_hdr_ver}
mkdir -p ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/include
cp -R include/asm-${LINTARCH} ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/include/asm
cp -R include/linux ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/include
touch ${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/include/linux/autoconf.h
cd ..
rm -rf %{linux_san_hdr_ver}


%Build
# See: http://www.embeddedtux.org/pipermail/etux.mbox/etux.mbox
# Remove memset.S for 8xx and 403, they have 4 word, not 8 word cache lines.
# memset.S incorrectly assumes an 8 word wide cache lines.
# Still a problem in glibc-2.3.2, see:
# http://ozlabs.org/pipermail/linuxppc-embedded/2004-June/014791.html
case ${CPU} in
        MPC823*) FPU_FLAG=no
                 rm sysdeps/powerpc/powerpc32/memset.S
                 ;;
        MPC860*) FPU_FLAG=no
                 rm sysdeps/powerpc/powerpc32/memset.S
                 ;;
        *) FPU_FLAG=yes
                 ;;
esac

# If the build is for an e500 toolchain then enable-add-ons in
# glibc cinfiguration needs to have the string spe added. - Stevep
if [ `echo ${TOOLCHAIN_PREFIX} | grep "gnuspe"` ]
then
  GLIBC_ADD_ONS="linuxthreads,spe"
else
  GLIBC_ADD_ONS="linuxthreads"
fi

# Temporary hack - stevep
# For building toolchain components an optimized version of the
# target is needed.  This should really be defined in the config
# area of ltib, and not done in the toolchain spec files.
# For now we assume that the optimised target can be derived by
# stripping the trailing "-" off the toolchain prefix, but this
# will not be true for all cases, eg when using uClibc toolchains.
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`

rm -rf build-glibc
mkdir build-glibc
cd build-glibc
CC="${TOOLCHAIN_PREFIX}gcc" BUILD_CC="${BUILDCC}" CFLAGS="-O" \
AR="${TOOLCHAIN_PREFIX}ar" RANLIB="${TOOLCHAIN_PREFIX}ranlib" \
../configure --prefix=/usr --build=%{_build} --host=${OPT_CFGHOST} \
--enable-kernel=2.4.3 --without-cvs --disable-profile --disable-debug \
--without-gd --without-tls --without-__thread --enable-shared \
--enable-add-ons=${GLIBC_ADD_ONS} --with-fp=${FPU_FLAG} \
--with-headers=${RPM_BUILD_ROOT}/%{pfx}/%{_prefix}/include
make LD="${TOOLCHAIN_PREFIX}ld" RANLIB="${TOOLCHAIN_PREFIX}ranlib"

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



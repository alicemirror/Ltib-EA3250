%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}
%define ppc_axe_driver ppc-axe-driver-20071127

Summary         : AXE driver for mpc5121
Name            : axe
Version         : 1.0
Release         : 1
License         : GPL/MIT
Vendor          : Freescale
Packager        : John Rigby
Group           : Drivers/Sound
Source          : %{name}-%{version}.tar.gz
Source1		: %{ppc_axe_driver}-1.zip
Patch1		: %{ppc_axe_driver}-fixes.patch
Patch2		: %{ppc_axe_driver}-Task-Context-Fixes.patch
Patch3		: %{ppc_axe_driver}-Loader-Null-symbol-Fix.patch
Patch4		: axe-1.0-allocation-debug.patch
Patch5		: axe_lib_update.patch
Patch6		: ppc-axe-driver-relocate.patch
Patch7		: %{ppc_axe_driver}-cache2.patch
Patch8		: %{ppc_axe_driver}-condvar.patch
Patch9		: %{ppc_axe_driver}-quiet.patch
Patch10		: axe-sample-codec-source-files.patch
Patch11		: axe-remove-codec-and-scheduler-binaries.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
# extract and patch the reference ppc_axe_driver
unzip ${RPM_SOURCE_DIR}/%{ppc_axe_driver}-1.zip
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

%Build
KSRC_DIR=${PKG_KERNEL_KBUILD_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT="$(eval echo $PKG_KERNEL_KBUILD_PRECONFIG)"
KBOUT=${KBOUT:-$KSRC_DIR}
echo $KBOUT
if [ ! -f $KBOUT/Makefile ]
then
    cat <<TXT
Expected to find a Makefile here:
$KBOUT/Makefile
to build kernel modules
TXT
    exit 1
fi
make KERNELDIR=$KBOUT clean
make -j1 KERNELDIR=$KBOUT

%Install
KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
rm -rf $RPM_BUILD_ROOT
KVER="`perl -e '$/ = ""; $_ = <>; m,VERSION\s*=\s*(\d)\s*PATCHLEVEL\s*=\s*(\d+)\s*SUBLEVEL\s*=\s*(\d+)\s*EXTRAVERSION[ \t]*=[ \t]*(\S*),m; print  "$1.$2.$3$4"' $KSRC_DIR/Makefile`"
DESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{base}
MODDESTDIR=$DESTDIR/lib/modules/$KVER/misc/
mkdir -p $MODDESTDIR
make install  DESTDIR=$DESTDIR MODDESTDIR=$MODDESTDIR

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


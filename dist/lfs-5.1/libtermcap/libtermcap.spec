%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A basic system library for accessing the termcap database.
Name            : libtermcap
Version         : 2.0.8
Release         : 31_1
License         : LGPL
Vendor          : Freescale Inc
Packager        : Steve Papacharalambous
Group           : System Environment/Libraries
Source          : termcap-2.0.8.tar.bz2
Patch0: termcap-2.0.8-shared.patch
Patch1: termcap-2.0.8-setuid.patch
Patch2: termcap-2.0.8-instnoroot.patch
Patch3: termcap-2.0.8-compat21.patch
Patch4: termcap-2.0.8-xref.patch
Patch5: termcap-2.0.8-fix-tc.patch
Patch6: termcap-2.0.8-ignore-p.patch
Patch7: termcap-buffer.patch
Patch8: termcap-2.0.8-bufsize.patch
Patch9: termcap-2.0.8-colon.patch
Patch10: libtermcap-aaargh.patch
Patch11: termcap-2.0.8-glibc22.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
The libtermcap package contains a basic system library needed to
access the termcap database.  The termcap library supports easy access
to the termcap database, so that programs can output character-based
displays in a terminal-independent manner.

%Prep
%setup -q -n termcap-2.0.8
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

%Build
if [ "$GNUTARCH" = m68knommu ]
then
   MAKEOPTS="TARGETS=libtermcap.a"
fi
make $MAKEOPTS

%Install
for i in usr/lib %{_infodir} usr/include etc lib
do
    mkdir -p ${RPM_BUILD_ROOT}/%{pfx}/$i
done

if [ "$GNUTARCH" = m68knommu ]
then
( cp libtermcap.a ${RPM_BUILD_ROOT}/%{pfx}/lib/
  cp termcap.h ${RPM_BUILD_ROOT}/%{pfx}/usr/include/
  cp termcap.info* ${RPM_BUILD_ROOT}/%{pfx}/%{_infodir}
  cd ${RPM_BUILD_ROOT}/%{pfx}
  cd ./%{_infodir}
  gzip -9nf ./termcap.info*
  chmod 644 ./termcap.info*
)

else
export PATH=/sbin:$PATH
make prefix=${RPM_BUILD_ROOT}/%{pfx}/usr install

install -c -m644 termcap.src ${RPM_BUILD_ROOT}/%{pfx}/etc/termcap
cp termcap.info* ${RPM_BUILD_ROOT}/%{pfx}/%{_infodir}

( cd ${RPM_BUILD_ROOT}/%{pfx}
  rm -f ./etc/termcap
  mv ./usr/lib/libtermcap.so* ./lib
  ln -sf libtermcap.so.2.0.8 ./lib/libtermcap.so.2
  ln -sf libtermcap.so.2 ./lib/libtermcap.so
  cd usr/lib
  ln -sf ../../lib/libtermcap.so.2.0.8 libtermcap.so
  cd ../..
  strip -R .comments --strip-unneeded ./lib/libtermcap.so.2.0.8
  cd ./%{_infodir}
  gzip -9nf ./termcap.info*
  chmod 644 ./termcap.info*
)
fi

%Clean
rm -rf ${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_DIR}/termcap-%{version}

%Files
%defattr(-,root,root)
%{pfx}/*



%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Secure Sockets Layer toolkit
Name            : openssl
Version         : 0.9.7g
Release         : 1
License         : BSD style
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
Patch0          : openssl-0.9.7g-sec.patch
Patch1          : openssl-0.9.7g-cf-include.patch
Patch2          : openssl-0.9.7g-linux-elf-m68k.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

The SEC patch is mcf547x_8x (coldfire) specific.

%Prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
case $ENDIAN in
    big)
        XTRA_OPTS="-DB_ENDIAN"
        ;;
    little)
        XTRA_OPTS="-DL_ENDIAN"
        ;;
    *)
        echo "Please set the ENDIAN environment variable to big|little"
        ;;
esac
case "$LINTARCH" in
    arm)
       OSSL_ARCH="linux-elf-arm"
       ;;
    m68k)
       OSSL_ARCH="linux-elf-m68k"
       ;;
    *)
       OSSL_ARCH="linux-$LINTARCH"
       ;;
esac

if [ -n "$PKG_OPENSSL_WANT_SEC" -a "$PLATFORM" = "mcf547x_8x" ]
then
   XTRA_OPTS="$XTRA_OPTS -DCF_SEC"
fi
./Configure $OSSL_ARCH --prefix=%{_prefix} shared no-asm $XTRA_OPTS
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
for i in lib %{_prefix}/lib %{_prefix}/sbin %{_prefix}/include
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/$i
done
VER="`perl -e '$_  = shift; chop; print' %{version}`"
for i in libcrypto.so libssl.so
do 
    cp -a $i.$VER $RPM_BUILD_ROOT/%{pfx}/%{base}/lib/
    ln -s ../../lib/$i.$VER $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/$i
done
cp -a apps/openssl $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/sbin
cp -Lr include/openssl $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

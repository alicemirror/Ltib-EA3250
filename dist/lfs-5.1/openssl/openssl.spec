%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Secure Sockets Layer toolkit
Name            : openssl
Version         : 0.9.8g
Release         : 1
License         : BSD style
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
Patch0          : openssl-md4_size_t.patch
Patch1          : openssl-md5_size_t.patch
Patch2          : openssl-sha_size_t.patch
Patch3          : openssl-0.9.8g-lib64.patch
Patch4          : openssl-0.9.8g-ripemd_size_t.patch
Patch5          : openssl-0.9.8g-sec.patch
Patch6          : openssl-0.9.8g-cryptodev.patch
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
    arm|m68k*)
       OSSL_ARCH="linux-generic32"
       ;;
    powerpc*)
       OSSL_ARCH="linux-ppc"
       ;;
    *)
       OSSL_ARCH="linux-$LINTARCH"
       ;;
esac
./Configure $OSSL_ARCH --prefix=%{_prefix} shared no-asm $XTRA_OPTS --with-cryptodev 
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
mkdir $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/pkgconfig
cp openssl.pc $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/pkgconfig/


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

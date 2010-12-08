%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : c++ libraries
Name            : boost
Version         : 1.39.0
Release         : 1
Vendor          : ltib.org
Packager        : Stuart Hughes/Mike Goins
Group           : System Environment/Libraries
Source          : %{name}_1_39_0.tar.bz2
License         : Boost (distributable)
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
Requires        : bzip2. zlib

%Description
%{summary}

%Prep
%setup -n %{name}_1_39_0

%Build
export PATH=$UNSPOOF_PATH 
./bootstrap.sh  --prefix=$RPM_BUILD_ROOT/%{pfx}/usr --libdir=$RPM_BUILD_ROOT/%{pfx}/usr/lib
export PATH=$SPOOF_PATH
echo "using gcc : $GNUTARCH : ${TOOLCHAIN_PREFIX}g++  ; " > tools/build/v2/user-config.jam
./bjam -d2 -q \
--toolset=gcc \
--layout=system \
--without-python \
-sZLIB_INCLUDE=$DEV_IMAGE/usr/include \
-sZLIB_LIBPATH=$DEV_IMAGE/usr/lib \
-sBZIP2_INCLUDE=$DEV_IMAGE/usr/include \
-sBZIP2_LIBPATH=$DEV_IMAGE/usr/lib \
stage


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/
./bjam -d2 -q \
--toolset=gcc \
--layout=system \
--without-python \
-sZLIB_INCLUDE=$DEV_IMAGE/include \
-sBZIP2_INCLUDE=$DEV_IMAGE/include \
install


%Clean
./bjam --clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

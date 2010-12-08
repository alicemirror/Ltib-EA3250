%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil}

Summary         : RTC test program
Name            : rtc-test
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Applications/Test
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
KSRC_DIR=${PKG_KERNEL_PATH_PRECONFIG:-$RPM_BUILD_DIR/linux}
KBOUT=${KBOUT:-$KSRC_DIR}
if [ ! -f $KSRC_DIR/Makefile ]
then
    cat <<TXT
You need a unpacked kernel source tree in:
$KSRC_DIR
to build this program
TXT
    exit 1
fi
pwd
echo KSRC_DIR is $KSRC_DIR
echo here in Prep
env | grep -i rtc
mkdir -p $RPM_PACKAGE_NAME
cd $RPM_PACKAGE_NAME
sed  '1,/-- 8< --/d' < $KSRC_DIR/Documentation/rtc.txt > rtc-test.c

%Build
cd $RPM_PACKAGE_NAME
env | grep -i rtc
make rtc-test
#make

%Install
cd $RPM_PACKAGE_NAME
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT/%{pfx}/usr/bin
mkdir -p $DESTDIR
cp -a rtc-test $DESTDIR

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


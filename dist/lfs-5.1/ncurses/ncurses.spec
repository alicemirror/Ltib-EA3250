%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : CRT screen handling and optimization package
Name            : ncurses
Version         : 5.3
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : ncurses-5.3.tar.gz
Patch0          : ncurses-5.3-etip-2.patch
Patch1          : ncurses-5.3-vsscanf.patch
Patch2          : ncurses-5.3-wint_t.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1 
%patch1 -p1
%patch2 -p1

%Build
CFLAGS="%{optflags} -DPURE_TERMINFO -DSVR4_CURSES"
%define optflags $CFLAGS
if [ "$GNUTARCH" != m68knommu ]
then
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
    --with-install-prefix=$RPM_BUILD_ROOT --mandir=%{_mandir} \
    --with-shared  --without-debug --without-cxx-binding --without-ada 
else
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
    --with-install-prefix=$RPM_BUILD_ROOT --mandir=%{_mandir} \
    --without-shared  --without-debug --without-cxx-binding --without-ada
fi
make -j1 HOSTCC="$BUILDCC"

sed -e 's%$srcdir/shlib tic$suffix%/usr/bin/tic$suffix%' \
misc/run_tic.sh > misc/run_tic.sh.tmp
mv misc/run_tic.sh misc/run_tic.sh.orig
mv misc/run_tic.sh.tmp misc/run_tic.sh

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx} includedir=%{_prefix}/include/ncurses libdir=%{_prefix}/lib mandir=%{_mandir}

if [ "$GNUTARCH" != m68knommu ]
then
chmod 755 $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.5.3
fi
#chmod 644 $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libncurses++.a
for i in curses.h eti.h form.h  menu.h ncurses.h panel.h term.h unctrl.h 
do 
    ln -sf ncurses/$i $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/$i
done
mv $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/tack.1 $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man1

if [ "$PKG_NCURSES_WANT_REDUCED_SET" = "y" ]
then
    echo "Only installing minimal terminfo, saving >5Meg"
    USR_SHARE=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share
    
    mv $USR_SHARE/terminfo $USR_SHARE/termtemp
    
    mkdir -p $USR_SHARE/terminfo/a
    mkdir -p $USR_SHARE/terminfo/d
    mkdir -p $USR_SHARE/terminfo/l
    mkdir -p $USR_SHARE/terminfo/r
    mkdir -p $USR_SHARE/terminfo/s
    mkdir -p $USR_SHARE/terminfo/v
    mkdir -p $USR_SHARE/terminfo/x
    
    cp -af $USR_SHARE/termtemp/a/ansi          $USR_SHARE/terminfo/a/
    cp -af $USR_SHARE/termtemp/a/ansi-m        $USR_SHARE/terminfo/a/
    cp -af $USR_SHARE/termtemp/d/dumb          $USR_SHARE/terminfo/d/
    cp -af $USR_SHARE/termtemp/l/linux         $USR_SHARE/terminfo/l/
    cp -af $USR_SHARE/termtemp/l/linux-m       $USR_SHARE/terminfo/l/
    cp -af $USR_SHARE/termtemp/r/rxvt          $USR_SHARE/terminfo/r/
    cp -af $USR_SHARE/termtemp/s/screen        $USR_SHARE/terminfo/s/
    cp -af $USR_SHARE/termtemp/s/screen-w      $USR_SHARE/terminfo/s/
    cp -af $USR_SHARE/termtemp/s/sun           $USR_SHARE/terminfo/s/
    cp -af $USR_SHARE/termtemp/v/vt52          $USR_SHARE/terminfo/v/
    cp -af $USR_SHARE/termtemp/v/vt100         $USR_SHARE/terminfo/v/
    cp -af $USR_SHARE/termtemp/v/vt102         $USR_SHARE/terminfo/v/
    cp -af $USR_SHARE/termtemp/v/vt200         $USR_SHARE/terminfo/v/
    cp -af $USR_SHARE/termtemp/x/xterm         $USR_SHARE/terminfo/x/
    cp -af $USR_SHARE/termtemp/x/xterm-color   $USR_SHARE/terminfo/x/
    cp -af $USR_SHARE/termtemp/x/xterm-xfree86 $USR_SHARE/terminfo/x/
    
    rm -rf $USR_SHARE/termtemp
fi

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Keytable files and keyboard utilities.
Name            : kbd
Version         : 1.08
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/System
Source          : kbd-1.08.tar.gz
Patch0          : kbd-1.08-more-programs.patch
Patch1          : kbd-1.08-chown.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1

%Build
./configure --prefix=%{_prefix}
perl -pi -e 's,ARCH=.*,ARCH=$ENV{LINTARCH},' make_include
echo "#define HAVE_locale_h" >> ./defines.h
if [ -z "$UCLIBC" ]
then
    echo "#define HAVE_libintl_h" >> ./defines.h
    echo '#define ENABLE_NLS' >> ./defines.h
fi
make

%Install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make install DESTDIR=$DESTDIR MANDIR=$DESTDIR/usr/share/man DATADIR=$DESTDIR//usr/share/kbd

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



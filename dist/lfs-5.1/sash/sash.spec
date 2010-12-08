%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : sash - Stand-Alone SHell by David I. Bell
Name            : sash
Version         : 1.1
Release         : 1
License         : GPL/Distributable
Vendor          : Freescale
Packager        : Matt Waddel
Group           : System Environment/Shell
Source          : sash-1.1-1.tar.gz
Patch0          : sash-1.1-1.Makefile.patch
Patch1          : sash-1.1-1144141552.patch
Patch2          : sash-1.1-hz.patch
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
make -j1 AR="${TOOLCHAIN_PREFIX}ar" RANLIB="${TOOLCHAIN_PREFIX}ranlib"


%Install
rm -rf $RPM_BUILD_ROOT
for i in bin sbin
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/$i
done
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
for f in reboot shutdown
do
    mv $RPM_BUILD_ROOT/%{pfx}/bin/$f $RPM_BUILD_ROOT/%{pfx}/sbin/$f
done

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



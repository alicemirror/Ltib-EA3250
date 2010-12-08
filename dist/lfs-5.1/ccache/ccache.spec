%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : C/C++ compiler cache
Name            : ccache
Version         : 2.4
Release         : 13
License         : GPL
Vendor          : Freescale
Packager        : LTIB addsrpms
Group           : Development/Tools
URL             : http://ccache.samba.org/
Source0         : http://samba.org/ftp/ccache/ccache-2.4.tar.gz
Source1         : ccache.bsh.in
Source2         : ccache.csh.in
Patch0          : ccache-html-links.patch
Patch1          : ccache-2.4-coverage-231462.patch
Patch2          : ccache-2.4-hardlink-doc.patch
Patch3          : ccache-2.4-noHOME-315441.patch
Patch4          : http://darkircop.org/ccache/ccache-2.4-md.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms ccache-2.4-13.fc9.src.rpm
from:
 http://download.fedora.redhat.com/pub/fedora/linux/releases/9/Fedora/source/SRPMS/

%Prep

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE1} > %{name}.sh
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE2} > %{name}.csh


%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make


%Install
rm -rf $RPM_BUILD_ROOT ccache-2.4.compilers
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{name}.sh %{name}.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/ccache
for name in %{compilers} ; do
  for c in $name %{_target_cpu}-%{_vendor}-%{_target_os}-$name ; do
    ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$c
    echo "%ghost %{_libdir}/ccache/$c" >> %{name}-%{version}.compilers
  done
done
install -dm 770 $RPM_BUILD_ROOT%{_var}/cache/ccache


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

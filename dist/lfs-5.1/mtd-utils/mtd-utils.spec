%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Memory Technology Device tools
Name		: mtd-utils
Version		: 20080618
Release		: 1
License		: GPL
Vendor		: Freescale
Packager	: Ross Wille
Group		: Applications/System
Source		: %{name}-%{version}.tar.bz2
Patch1		: mtd-utils-20060302-cf-byteswap_h-1.patch
Patch2		: mtd-utils-20060302-eraseall.patch
Patch3		: mtd-utils-20060302-eraseall_prog.patch
Patch4		: mtd-utils-20080618-pres-int-files.patch
Patch5		: mtd-utils-20080618-macro-incr.patch
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

Extracted source from the git tree: 
  git clone git://git.infradead.org/mtd-utils.git
  SHA1 d769da93a56590c23ce9430a1d970e31e835ae88

%Prep
%setup -n %{name}
%patch1 -p1
%patch2 -p2
%patch3 -p2
%patch4 -p1
%patch5 -p1

%Build
make -j1 WITHOUT_XATTR=1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 DESTDIR=$RPM_BUILD_ROOT/%{pfx} SBINDIR=%{_prefix}/bin MANDIR=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd
install -m0644 include/mtd/*.h $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

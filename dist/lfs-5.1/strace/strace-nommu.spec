%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : trace system calls associated with a running process
Name            : strace
Version         : 4.4.98
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Debuggers
Source          : %{name}-%{version}.tar.bz2
Patch0          : strace-4.4.98-fixarm.patch
Patch1          : strace-4.4.98-sysctl_h.patch
Patch2          : strace-4.4.98-sysctl_h_fixup.patch
Patch3          : strace-4.4.98-mem_c_fixup.patch
Patch4          : strace-4.4.98-quota_fixes-2.patch
Patch5          : strace-4.4.98-1155222257.patch
Patch6          : strace-4.4.98-nommu-1.patch
Patch7          : strace-4.4.98-4.2-fixes.patch
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
%patch7 -p1

%Build
case "$PLATFORM" in
    m520xevb|m532xevb)
        # this is only needed for an older brokenish toolchain
        PLATFORM_CFLAGS="-DHZ=100"
        ;;
    *)
        PLATFORM_CFLAGS=
        ;;
esac
ac_cv_header_asm_sigcontext_h=yes \
CFLAGS="$PLATFORM_CFLAGS" \
./configure --prefix=%{_prefix} --host=m68k-linux --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

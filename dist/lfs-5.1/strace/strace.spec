%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : trace system calls associated with a running process
Name            : strace
Version         : 4.5.14
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Debuggers
Source          : %{name}-%{version}.tar.bz2
Patch0          : strace-4.5.14-syscall_eabi.patch
Patch1          : strace-fix-arm-bad-syscall.patch
Patch2          : strace-4.5.14-glibc_2.5-1.patch
Patch3          : strace-4.5.14-kernel_headers_2.6.18-1.patch          
Patch4          : strace-4.4.98-1155222257.patch
Patch5          : strace-4.5.14-linux-dirent.patch
Patch6          : strace-arm-no-cachectl.patch
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
# Note strace-4.4.98-1155222257.patch and ac_cv_header_asm_sigcontext_h=yes
# is needed for mcf547x_8x (rigoletto) to work around a toolchain
# with poorly sanitised headers.  It should not affect other platforms.
ac_cv_header_asm_sigcontext_h=yes \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

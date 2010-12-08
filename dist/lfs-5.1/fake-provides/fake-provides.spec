# These are horrible hacks to take care of the fact that some
# packages do indeed depend directly on some things outside the
# root file system.

%define __os_install_post %{nil}
%define  pfx /opt/freescale/rootfs/%{_target_cpu}

Name     : fake-provides
Version  : 1.0
Release  : 5
Group    : Bootstrap
Summary  : Fake provides to satisfy package dependancies
License  : GPL
Packager : Stuart Hughes, Steve Papacharalambous
Vendor   : Freescale Corp
Buildroot: /tmp/%{name}-%{version}
Prefix   : %{pfx}

Provides : /bin/sh
Provides : /bin/bash
Provides : /bin/csh
Provides : /bin/tcsh
Provides : /usr/bin/env
Provides : /usr/bin/perl
Provides : /usr/local/bin/perl
Provides : libgcc_s.so.1
Provides : libgcc_s.so.1(GCC_3.0)
Provides : libgcc_s.so.1(GLIBC_2.0)
%ifarch ppc ppc64
Provides : linux-vdso32.so.1
%endif
%ifarch ppc64
Provides : linux-vdso64.so.1
%endif
Provides : /bin/gawk
Provides : /usr/bin/nawk
Provides : /usr/bin/awk
Provides : /usr/bin/bash
Provides : perl 5.8.0
Provides : perl(Getopt::Long)
Provides : perl(Getopt::Std)
Provides : perl(constant)
Provides : perl(getopts.pl)
Provides : perl(strict)
Provides : perl(vars)
Provides : perl(Carp)
Provides : perl(Cwd)
Provides : perl(Data::Dumper)
Provides : perl(DynaLoader)
Provides : perl(Exporter)
Provides : perl(File::Basename)
Provides : perl(File::Compare)
Provides : perl(File::Copy)
Provides : perl(File::Find)
Provides : perl(File::Spec)
Provides : perl(File::stat)
Provides : perl(IO::File)
Provides : perl(POSIX)
Provides : perl(Text::ParseWords)
Provides : libstdc++.so.5
Provides : libstdc++.so.5(CXXABI_1.2)
Provides : libstdc++.so.5(GLIBCPP_3.2)
Provides : libstdc++.so.5(GLIBCPP_3.2.1)
Provides : /bin/rm
Provides : /sbin/ldconfig
Provides : /sbin/chkconfig
Provides : linux-gate.so.1

%Description

These are horrible hacks to take care of the fact that some
packages do indeed depend directly on some things outside the
root file system.  This is unavoidable unless we change the packages.


%Prep

%Build

%install
rm -rf $RPM_BUILD_ROOT

%Clean
rm -rf $RPM_BUILD_ROOT

%Files


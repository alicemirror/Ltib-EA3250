%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A debugging and profiling tool
Name            : valgrind
Version         : 3.3.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Rigby
Group           : Development/Debuggers
URL		: http://valgrind.org/downloads/valgrind-3.3.1.tar.bz2 
Source          : %{name}-%{version}.tar.bz2
Patch1          : valgrind-3.3.1-8xx.patch
Patch2          : valgrind-3.3.1-softfloat-02.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch1 -p1
%patch2 -p1

%Build
#./configure --disable-tls --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir} 
./configure --enable-tls --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} --mandir=%{_mandir} 

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

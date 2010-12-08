%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : API to load and control interpreted programs 
Name            : embryo
Version         : 0.9.9.050
Release         : 1
License         : BSD
Vendor          : The Enlightenment Project (http://www.enlightenment.org/)
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.enlightenment.org/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
Embryo is primarily a shared library that gives you an API to load and control
interpreted programs compiled into an abstract machine bytecode that it
understands.  This abstract (or virtual) machine is similar to a real machine
with a CPU, but it is emulated in software.  The architecture is simple and is
the same as the abstract machine (AMX) in the
<a href=http://www.compuphase.com/pawn.htm>PAWN</a> language (formerly called
SMALL) as it is based on exactly the same code. Embryo has modified the code
for the AMX extensively and has made it smaller and more portable.  It is VERY
small.  The total size of the virtual machine code AND header files is less
than 2500 lines of code.  It includes the floating point library support by
default as well.  This makes it one of the smallest interpreters around, and
thus makes is very efficient to use in code.

%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/ -name "*.la" | xargs rm -f

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


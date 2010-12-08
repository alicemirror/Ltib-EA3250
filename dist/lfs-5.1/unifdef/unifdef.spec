%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Unifdef tool for removing ifdef'd lines from c/c++
Name            : unifdef
Version         : 1.0
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
URL             : http://www.cs.cmu.edu/~ajw/public/dist/unifdef-1.0.tar.gz
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
make clean
make

%Install
rm -rf $RPM_BUILD_ROOT
for i in bin man/man1
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/$i
done
make install DEST=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __unzip unzip -a

Summary         : Xerces-C++ validating XML parser
Name            : xerces-c
Version         : 2.2.0
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : xerces-c-src2_2_0.zip
License         : Apache
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup -n xerces-c-src2_2_0

%Build
export XERCESCROOT=$RPM_BUILD_DIR/xerces-c-src2_2_0
cd src/xercesc
sh runConfigure -p linux -z -fpermissive  -P%{_prefix}
make
#make SHLIBSUFFIX=-mw.so

%Install
rm -rf $RPM_BUILD_ROOT
export XERCESCROOT=$RPM_BUILD_DIR/xerces-c-src2_2_0
cd src/xercesc
make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
#ln -s libxerces-c.so.22 $RPM_BUILD_ROOT/%{_prefix}/lib/libxerces-c-mw.so.22
#ln -s libxerces-c.so $RPM_BUILD_ROOT/%{_prefix}/lib/libxerces-c-mw.so

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Guarana framework
Name            : guarana
Version         : 0.1.0.1
Release         : 1
License         : BSD
Vendor          : ProFUSION embedded systems <contact@profusion.mobi>
Packager        : ProFUSION embedded systems <contact@profusion.mobi>
Group           : System Environment/Libraries
URL             : http://www.profusion.mobi/
Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : eet evas ecore embryo

%Description
Guarana is a framework to help with Graphical User Interface
applications, providing signals, widgets, an easy to use
Model-View-Controller set of classes and possible more.

Guarana is built on top of excellent Enlightenment Foundation
Libraries, but we try to keep as much as possible platform-independent
where possible (ie: not the widgets).


%Prep
%setup

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


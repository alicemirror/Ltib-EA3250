%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Message bus system for applications to talk to one another
Name            : dbus
Version         : 1.2.6
Release         : 1
License         : AFLv2.1 or GPLv2
Vendor          : Free Desktop
Packager        : Thierry Pierret/Stuart Hughes/Tarek Allaoua
Group           : Development/Libraries
URL             : http://dbus.freedesktop.org
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 

%Build
# Note --with-xml could also specify libxml
config_opts='ac_cv_have_abstract_sockets=yes'
extra_opts='--with-xml=expat --without-x --enable-tests=no --enable-selinux=no'

eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            $extra_opts

# Avoid libtool searching in /usr/lib
perl -pi -e 's,^sys_lib_search_path_spec=.*,sys_lib_search_path_spec=,' libtool
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

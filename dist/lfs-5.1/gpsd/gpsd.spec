%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : gpsd - A GPS service daemon
Name            : gpsd
Version         : 2.37
Release         : 1
License         : BSD
Vendor          : Freescale
Packager        : Duck
Group           : Applications/System
URL             : http://gpsd.berlios.de/
Source          : %{name}-%{version}.tar.gz
Patch1          : gpsd-2.37-for-uclinux.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}


%Description
%{summary}

%Prep
%setup 
%patch1 -p1

%Build


# If python support is not configured, don't build the
# python pieces.
#
# If python support is configured, figure out the version
# of the target's python, so that our python pieces can
# be installed in the proper directories.

if [ "$PKG_GPSD_WANT_PYTHON" != "y" ]; then
    _python_opt="--disable-python"
else
    _py_ver=$(rpm --dbpath %{_dbpath} -q python | \
    	perl -n -e 'm,python-(\d+\.\d+), and do { print $1 }')
fi

# X11 is currently unsupported.  To add it,
# add this option to packages.lkc
# For now, it's always disabled

if [ "$PKG_GPSD_WANT_X11" != "y" ]; then
    _x11_opt="--disable-X11 --without-x"
fi

if [ "$GNUTARCH" = m68knommu ]; then
am_cv_python_version=${_py_ver}  \
am_cv_python_pythondir="\${prefix}/lib/python${_py_ver}/site-packages" \
am_cv_python_pyexecdir="\${exec_prefix}/lib/python${_py_ver}/site-packages" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	$_python_opt $_x11_opt --without-dbus --disable-shared
else
am_cv_python_version=${_py_ver}  \
am_cv_python_pythondir="\${prefix}/lib/python${_py_ver}/site-packages" \
am_cv_python_pyexecdir="\${exec_prefix}/lib/python${_py_ver}/site-packages" \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
	$_python_opt $_x11_opt --without-dbus
fi

make all

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : keyfuzz - Manipulate a keyboard input driver's keycode translation table
Name            : keyfuzz
Version         : 0.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Faith
Group           : System Environment/Utilities
Source          : keyfuzz-0.2.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://0pointer.de/lennart/projects/keyfuzz/

%Description
%{summary}
Allows remapping keys in the input subsystem driver using ioctls on the
/dev/input/event* node.  See the section on EVIOCGKEYCODE/EVIOCSKEYCODE in
linux/Documentation/input/input-programming.txt.
Display keymap with: keyfuzz -g > keyMap
Modify keymap with: keyfuzz -s < newKeyMap

%Prep
%setup 

%Build
ac_cv_func_malloc_0_nonnull=yes \
./configure --prefix=%{_prefix} --bindir=/bin --host=$CFGHOST --build=%{_build} --mandir=%{_mandir}
make 

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*


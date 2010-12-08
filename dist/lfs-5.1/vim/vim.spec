%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : vim - vi much improved
Name            : vim
Version         : 6.2
Release         : 1
License         : Vim (Distributable)
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Editors
Source          : vim-6.2.tar.bz2
Patch0          : vim-6.2-crossbuild.patch
Patch1          : vim-6.2-tputs-tgoto.patch
Patch2          : vim-6.2-awk.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n vim62
%patch0 -p1
%patch1 -p1
%patch2 -p1


%Build
ac_cv_func_putenv=yes ac_cv_sizeof_int=4 \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --disable-gui --disable-gpm --without-x --with-tlib=ncurses \
            --mandir=%{_mandir}
make -j1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : MySQL SQL database, client programs and shared library
Name            : mysql
Version         : 4.1.12
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Jason Jin
Group           : System Environment/Daemons
Source          : %{name}-%{version}.tar.gz
Patch0          : %{name}-%{version}-fsl.patch
Patch1          : mysql-4.1.12-gcc-4.2.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n  %{name}-%{version}
%patch0 -p1
%patch1 -p1

%Build
./configure --prefix=/usr --host=$CFGHOST --build=%{_build} \
	--enable-so	\
	--with-named-curses-libs=-lncurses	\
	--without-man	\
	--without-docs	\
	ac_cv_sys_restartable_syscalls=${ac_cv_sys_restartable_syscalls='no'}	\
	ac_cv_conv_longlong_to_float=yes   \
	--with-zlib	

make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
cd $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/mysql
mv $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/mysql/* ../
rm mysql -rf
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



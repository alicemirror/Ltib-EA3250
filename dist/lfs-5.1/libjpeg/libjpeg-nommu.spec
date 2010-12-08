%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library for manipulating JPEG image format files
Name            : libjpeg
Version         : 6b
Release         : 1
License         : Distributable
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source          : jpegsrc.v6b.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n jpeg-6b
# support opteron build host
perl -pi -e 's,f301-\*\),f301-* | x86_64-*),' config.sub

%Build
export PATH=$UNSPOOF_PATH
./configure --enable-static --target=$CFGHOST --prefix=%{_prefix}
export PATH=$SPOOF_PATH
make

%Install
rm -rf $RPM_BUILD_ROOT
for i in include lib bin man/man1
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/$i
done
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
make install-lib prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A library for decoding mpeg-2 and mpeg-1 video streams.
Name            : libmpeg2
Version         : 0.4.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : John Faith
Group           : System Environment/Libraries
Source          : mpeg2dec-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://libmpeg2.sourceforge.net

%Description
%{summary}

%Prep
%setup -n mpeg2dec-%{version}

%Build
./configure --enable-shared --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*



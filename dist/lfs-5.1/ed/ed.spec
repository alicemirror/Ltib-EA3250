%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNU line editor
Name            : ed
Version         : 0.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Text
Source          : ed-0.2.tar.gz
Patch0          : ed-0.2-mkstemp.patch
Patch1          : ed-0.2-mandir.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch0 -p1
%patch1 -p1

%Build
ac_cv_header_stdc=yes ./configure --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



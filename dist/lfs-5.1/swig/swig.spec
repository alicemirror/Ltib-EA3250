%define pfx /opt/freescale/rootfs/%{_target_cpu}

######################################################################
# Usually, nothing needs to be changed below here between releases
######################################################################
Summary         : Simplified Wrapper and Interface Generator
Name            : swig
Version         : 1.3.21
Release         : 1
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
License         : BSD
BuildRoot       : %{_tmppath}/%{name}

%Description
%{summary}

%Prep
%setup -n SWIG-%{version}

%Build
cat <<'EOF' > config.cache
ac_cv_have_x=${ac_cv_have_x='have_x=yes ac_x_includes=%{_prefix}/X11R6/include ac_x_libraries=%{_prefix}/X11R6/lib'}
EOF
./configure --cache-file=config.cache --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/%{_prefix}/bin/*
%{pfx}/%{_prefix}/lib/swig*

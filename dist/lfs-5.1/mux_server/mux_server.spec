%define pfx /opt/freescale/rootfs/%{_target_cpu}

Name:           mux_server
Version:        1.0
Release:        1
Summary:        Create and remove virtual network interfaces

Group:          Applications/System
License:        LGPL
Source0:        mux_server.c
Patch0          : mux_sever-1.0-fs-decl.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%description
serial console (de)multiplexor program


%prep
%setup -T -c -n %{name}-%{version}
%{__cp} %{SOURCE0} mux_server.c
%patch0 -p1

%build
%{__cc} %{optflags} -lpthread mux_server.c -o mux_server


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
install -d $RPM_BUILD_ROOT
install -m 755 mux_server $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{pfx}/%{_prefix}/bin/mux_server

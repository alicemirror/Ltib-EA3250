%define pfx /opt/freescale/rootfs/%{_target_cpu}

Name:           tunctl
Version:        1.5
Release:        1
License:        GPL
Vendor:         ltib.org
Group:          Applications/System
Summary:        Create and remove virtual network interfaces
URL:            http://www.user-mode-linux.org/
Source0:        %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%description
Virtual network interface manipulation tool from User Mode Linux project.
This is from http://tunctl.sourceforge.net/

%prep
%setup

%build
gcc tunctl.c -o tunctl

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin
install -d $RPM_BUILD_ROOT
install -m 755 tunctl $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{pfx}/%{_prefix}/bin/tunctl

%changelog
* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4-2
- Move to sbin (Marek Mahut, #434583)

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4-1
- Initial packaging

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Python serial handling module
Name            : pyserial
Version         : 2.1
Release         : 2
License         : Python
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
Source          : %{name}-%{version}.zip
Patch0          : %{name}-cux.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch0 -p1

%Build
python setup.py build

%Install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT/%{pfx} --record=file_list

%Clean
rm -rf $RPM_BUILD_ROOT


%Files -f file_list
%defattr(-,root,root)



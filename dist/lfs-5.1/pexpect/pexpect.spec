%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Python expect module
Name            : pexpect
Version         : 0.98
Release         : 2
License         : Python Software Foundation License
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
Source          : %{name}-%{version}.tgz
Patch0          : pexpect-8nov04.patch 
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}
%patch0

%Build
python setup.py build

%Install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT/%{pfx} --record=file_list

%Clean
rm -rf $RPM_BUILD_ROOT


%Files -f file_list
%defattr(-,root,root)



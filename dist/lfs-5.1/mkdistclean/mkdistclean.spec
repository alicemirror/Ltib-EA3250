%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define __os_install_post %{nil} 
%define __check_files %{nil}

Summary         : Package used to clean out ltib rootfs
Name            : mkdistclean
Version         : 1.0
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/System
#Source          : %{name}-%{version}.tar.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
#%setup 

%Build

%Install
: ${DEV_IMAGE:?Please set the path to the area to remove}
if [ ! -d $DEV_IMAGE ] ; then
    echo "$DEV_IMAGE is not a directory"
    exit 1
fi
if [ $DEV_IMAGE = '/' ] ; then
    echo "$DEV_IMAGE is not allowed"
    exit 1
fi
if [ $EUID = 0 ] ; then
    echo "root cannot run this"
    exit 1
fi
if [ ! -O $DEV_IMAGE ] ; then
    echo "you are not the owner of $DEV_IMAGE"
    exit 1
fi
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
cd  $DEV_IMAGE
(
set +e
find -type d -exec mkdir -p $RPM_BUILD_ROOT/%{pfx}/{} \;
find . ! -type d -exec touch $RPM_BUILD_ROOT/%{pfx}/{} \;
exit 0
)
mkdir -p $RPM_BUILD_ROOT/%{pfx}/root/.ssh
touch $RPM_BUILD_ROOT/%{pfx}/root/.ssh/known_hosts
touch $RPM_BUILD_ROOT/%{pfx}/.ash_history

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/.ash_history
%{pfx}/*

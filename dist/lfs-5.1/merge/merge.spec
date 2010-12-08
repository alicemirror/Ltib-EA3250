%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Merge files for an embedded root filesystem
Name            : merge
Version         : 0.1
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Steve Papacharalambous/Stuart Hughes
Group           : System Environment/Utilities
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
# We have assume the user knows merge file dependencies.
Autoreqprov     : no

%Description
Detects the presence of of merge directory in the top level of the root
file system builder directory, and if it is present creates a rpm containing
the directory structure and files beneath the merge directory.
The purpose of this is to allow the user to add files and directories
that will get included in the target root file system.


%Prep

%Build

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
touch $RPM_BUILD_ROOT/%{pfx}/etc/ltib-release

for dir in "$PLATFORM_PATH/merge" "$TOP/merge"
do
    if [ -d $dir ]
    then
        cd $dir
        find . \( -name CVS -o -name .svn -o -name .git \) -prune -o -perm -444 ! -type b ! -type c -print0 2>/dev/null |  cpio -p0d  --quiet $RPM_BUILD_ROOT/%{pfx}
        cd -
    fi
done

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%attr(0777, root, root) %{pfx}/etc/ltib-release
%{pfx}/*

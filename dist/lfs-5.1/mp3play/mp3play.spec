%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : mp3play - A simple mp3player
Name            : mp3play
Version         : 1.0
Release         : 0
License         : GPL
Vendor          : Freescale
Packager        : Matt Waddel
Group           : Applications/System
Source          : mp3play-%{version}-%{release}.tar.gz
Patch1          : mp3play-autoconf-1.0.patch
Patch2          : mp3play-1.0-ppc-fixes.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

This package comes from the uClinux.org CVS repository:
cvs.uclinux.org:/var/cvs/uClinux-dist/user/mp3play

%Prep
%setup -n mp3play
%patch1 -p1
%patch2 -p1

%Build
if gcc -dM -E -xc /dev/null | grep -q __mcoldfire__
then
     DEFS="CONFIG_COLDFIRE=1"
fi
if [ "$ENDIAN" = "big" ]
then
     DEFS="$DEFS BIG_ENDIAN=1"
else
     DEFS="$DEFS LITTLE_ENDIAN=1"
fi

make $DEFS


%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr/bin
cp mp3play $RPM_BUILD_ROOT/%{pfx}/usr/bin

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : IOZONE filesystem Benchmark tool.
Name            : iozone
Version         : 3
Release         : 281
License         : Freeware
Vendor          : Freescale
Packager        : Rakesh S Joshi
Group           : Application/Engineering
Source          : %{name}%{version}_%{release}.tar
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}%{version}_%{release}

%Build
cd src/current/
if [ "$GNUTARCH" = arm ]
then
perl -pi -e 's,(linux-arm:\t.*),\1 fileop_linux-arm.o,' makefile
fi
if [ "$GNUTARCH" = m68k ]
then
  make linux
else
  make linux-${GNUTARCH}
fi

%Install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/%{name}%{version}_%{release}/src/current
mkdir -p $RPM_BUILD_ROOT/%{pfx}/bin/
cp iozone $RPM_BUILD_ROOT/%{pfx}/bin/
cp fileop $RPM_BUILD_ROOT/%{pfx}/bin/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

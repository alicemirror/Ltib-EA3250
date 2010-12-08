%define base %(echo %{_prefix} | sed -e s,/usr.*$,,)
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : System logging and kernel message trapping daemons
Name            : sysklogd
Version         : 1.4.1
Release         : 1
License         : GPL/BSD
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : sysklogd-1.4.1.tar.gz
Patch0          : sysklogd-1.4.1-man.patch
Patch1          : sysklogd-1.4.1-kernel_headers-1.patch
Patch2          : sysklogd-1.4.1-permissions.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
make RPM_OPT_FLAGS=

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{base}/sbin
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man5
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_mandir}/man8
make BINDIR=$RPM_BUILD_ROOT/%{pfx}/%{base}/sbin MANDIR=$RPM_BUILD_ROOT/%{pfx}/%{_mandir} install
cat > $RPM_BUILD_ROOT%{pfx}/etc/syslog.conf << "EOF"
# Begin /etc/syslog.conf

auth,authpriv.* -/var/log/auth.log
*.*;auth,authpriv.none -/var/log/sys.log
daemon.* -/var/log/daemon.log
kern.* -/var/log/kern.log
mail.* -/var/log/mail.log
user.* -/var/log/user.log
*.emerg *

# End /etc/syslog.conf
EOF

chmod 644 $RPM_BUILD_ROOT%{pfx}/etc/syslog.conf

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



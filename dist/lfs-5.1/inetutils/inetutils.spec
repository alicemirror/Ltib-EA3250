%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Networking utilities
Name            : inetutils
Version         : 1.4.2
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Base
Source          : inetutils-1.4.2.tar.gz
Patch1          : inetutils-1.4.2-rm_tftp_h.patch
Patch2          : inetutils-1.4.2-gcc4_fixes-2.patch
Patch3          : inetutils-1.4.2-gcc-4.3.patch
Patch4          : inetutils-1.4.2-ruserpass-uclibc.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%Build
./configure --prefix=%{_prefix} --disable-syslogd \
     --libexecdir=%{_prefix}/sbin --disable-logger \
     --sysconfdir=%{_sysconfdir} \
     --disable-whois --host=$CFGHOST --build=%{_build} \
     --with-ncurses-include-dir=none --mandir=%{_mandir} \
     --with-PATH_LOGIN="/bin/login"

make

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx} install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/bin
mv $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/ping $RPM_BUILD_ROOT/%{pfx}/bin/ping
# remove the man pages that will conflict with sysklogd package
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man/man5/syslog.conf.5 
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/share/man/man8/syslogd.8


%Clean
rm -rf $RPM_BUILD_ROOT


%Files

# Notes: The preferred ftp daemon is vsftpd, and the ftpd daemon in this
#        package is a bogon and should not be used.  Really copying it to
#        the rootfs should be prevented in this section.
#        - Stevep
#
#        When inetd is started without specifying the config file on the
#        command line an error is logged in the system log file complaining
#        that the directory /etc/inet.d does not exist.  For example:
#        "Sep  8 12:30:58 <hostname> daemon.err inetd[<pid>]:
#         /etc/inetd.d: No such file or directory"
#        This is because the inetd daemon reads /etc/inetd.conf and then
#        /etc/inet.d/* and complains if it can't locate both.  However,
#        provided that /etc/inetd.conf exists then the inetd daemon functions
#        correctly and the error message can be ignored.
#        If needed the error message can be eliminated by giving the config
#        file on the inetd invocation line, e.g. ;
#        /usr/sbin/inetd -R 1000 /etc/inetd.conf
#        - Stevep
%defattr(-, root, root)
%attr(755, root, root) %{pfx}/%{_prefix}/bin/rsh
%attr(755, root, root) %{pfx}/%{_prefix}/bin/rlogin
%attr(755, root, root) %{pfx}/%{_prefix}/bin/rcp
%attr(4755, root, root) %{pfx}/bin/ping
%{pfx}/*


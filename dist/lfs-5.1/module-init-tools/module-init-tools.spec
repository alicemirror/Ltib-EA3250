%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define prever pre5

Summary: Linux 2.6 kernel module management utilities.
Name: module-init-tools
Version: 3.1
Release: 0.%{prever}.3
License: GPL
Vendor: Freescale Inc.
Packager: Steve Papacharalambous
Group: System Environment/Kernel
Source: module-init-tools-%{version}-%{prever}.tar.bz2
Source1: module-init-tools-%{version}-%{prever}.tar.bz2.sign
Source2: modprobe.conf.dist
Patch1: module-init-tools-defconfig.patch
Exclusiveos: Linux
#Prereq: /sbin/chkconfig sh-utils
Obsoletes: modules modutils-devel modutils
Provides: modutils = %{version}
# BuildPrereq: zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}

Prefix: %{pfx}

%description
Module loading for the Linux kernel for 2.6 kernels.
For older kernels use the modutils package.

%prep
%setup -q -n module-init-tools-%{version}-%{prever}
%patch1 -p1 -b .dist

%build
# insmod.static (diet)
# %ifarch i386
# if [ -x /usr/bin/diet ]; then
#   export CC="diet gcc"
# fi
# %endif

# Note: module-init-tools is not backward compatbile, if you remove
# DCONFIG_NO_BACKWARDS_COMPAT, it will just try to run 'prog.old'
# so you'll need to have modutils installed
export CFLAGS="-Os -g -DCONFIG_NO_BACKWARDS_COMPAT=1"
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build}
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/sbin
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx} sbindir=/sbin bindir=/sbin mandir=/usr/share/man

install -m 755 generate-modprobe.conf \
 $RPM_BUILD_ROOT/%{pfx}/sbin

mkdir -p $RPM_BUILD_ROOT/%{pfx}/etc
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{pfx}/etc/modprobe.conf.dist

#find $RPM_BUILD_ROOT/%{pfx}/sbin/ -name '*.static' -exec rm {} \;

#mv $RPM_BUILD_ROOT/%{pfx}/%{_bindir}/lsmod $RPM_BUILD_ROOT/%{pfx}/sbin

#install -m 755 insmod-static $RPM_BUILD_ROOT/%{pfx}/sbin/insmod.static

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}-%{prever}

# %post
# get rid of the old installations on upgrade
# if [ -x /etc/rc.d/init.d/kerneld ] ; then
#     /sbin/chkconfig --del kerneld
# fi
# if [ -f /etc/conf.modules -a ! -f /etc/modules.conf ] ; then
#    mv -f /etc/conf.modules /etc/modules.conf
# fi
# if [ -f /etc/modules.conf -a ! -f /etc/modprobe.conf ] ; then
#    echo "# Note: for use under 2.4, changes must also be made to modules.conf!" >/etc/modprobe.conf
#    /sbin/generate-modprobe.conf --stdin < /etc/modules.conf >> /etc/modprobe.conf 2>/dev/null
#    chmod 644 /etc/modprobe.conf
#    echo "# Note: for use under 2.6, changes must also be made to modprobe.conf!" >> /etc/modules.conf
# fi

%files
%defattr(-,root,root)
# /etc/modprobe.conf.dist
# /sbin/*
# %{_mandir}/*/*
%{pfx}/*

%changelog
* Wed Sep 22 2004 Bill Nottingham <notting@redhat.com> 3.1-0.pre5.3
- add rule for emu10k1 synth (#133280)

* Wed Sep  1 2004 Bill Nottingham <notting@redhat.com> 3.1-0.pre5.2
- fix segfault (#131441)

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> 3.1-0.pre5.1
- update to 3.1-pre5

* Thu Aug 26 2004 Bill Nottingham <notting@redhat.com> 3.0-2
- more modprobe.conf.dist sound tweaks

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Bill Nottingham <notting@redhat.com> 3.0-0.pre10.1
- remove back compat, rename to module-init-tools

* Wed May  5 2004 Bill Nottingham <notting@redhat.com> 2.4.26-16
- fix sound restoring on module load when done via OSS compat

* Thu Apr 15 2004 Bill Nottingham <notting@redhat.com> 2.4.26-15
- don't buildreq autoconf-2.13 (#116770)
- sound-slot-0/snd-card-0 hacking-around

* Mon Mar 29 2004 Bill Nottingham <notting@redhat.com> 2.4.26-14
- modinfo: use new modinfo if passed <foo>.ko

* Tue Mar 23 2004 Steve Dickson <SteveD@RedHat.com>
- Added the mounting of /proc/fs/nfsd to modprobe.conf.dist
  so it gets mounted when nfsd is loaded.

* Tue Mar 16 2004 Steve Dickson <SteveD@RedHat.com>
- /var/lib/nfs/rpc_pipefs not /var/lib/rpc_pipes should be
  mounted when sunrpc is loaded.

* Fri Mar 12 2004 Steve Dickson <SteveD@RedHat.com>
- umount rpc_pipefs when sunrpc is unloaded

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 2.4.26-9
- add nfsv4 aliases to modprobe.conf.dist
- clean out upstreamed aliases in modprobe.conf.dist
- mount rpc_pipefs when sunrpc is loaded

* Fri Mar  5 2004 Bill Nottingham <notting@redhat.com> 2.4.26-7
- blacklist eth1394 (#117383)

* Mon Feb 23 2004 Bill Nottingham <notting@redhat.com> 2.4.26-6
- update module-init-tools to 3.0pre10
- fix modinfo (#116305)
- always include /etc/modprobe.conf.dist (don't require the line in modprobe.conf)
- ship a static modprobe.conf.dist, don't generate it at build time
- clean up modprobe.conf.dist a little (#113772, #113768)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Bill Nottingham <notting@redhat.com>
- don't use trampolines in insmod, working around #106005

* Thu Jan 29 2004 Bill Nottingham <notting@redhat.com> 2.4.26-3
- fix irda (#114268), bluetooth (#114019) and alsa aliases

* Tue Dec 16 2003 Bill Nottingham <notting@redhat.com> 2.4.26-2
- add OSS compat ALSA module aliases for 2.6

* Mon Dec 15 2003 Bill Nottingham <notting@redhat.com> 2.4.26-1
- update to 2.4.26
- switch around man pages; the module-init-tools man pages are now
  the default
- add backwards compat usb aliases for the simple case
- add some commentary to modules.conf/modprobe.conf on conversion
- modutils-devel goes away

* Tue Oct  7 2003 Bill Nottingham <notting@redhat.com> 2.4.25-13
- fix handling of updates path (#106482)

* Tue Sep 30 2003 Bill Nottingham <notting@redhat.com> 2.4.25-12
- add modprobe.conf(5) (#105760, <salimma1@yahoo.co.uk>)

* Tue Sep 30 2003 Bill Nottingham <notting@redhat.com> 2.4.25-11
- update to module-init-tools-0.9.14, enable zlib, adjust patches

* Thu Sep 25 2003 Bill Nottingham <notting@redhat.com> 2.4.25-10
- provide module-init-tools

* Mon Sep  8 2003 Bill Nottingham <notting@redhat.com> 2.4.25-9
- fix bluetooth typo (#88859)
- add viocd alias (#89232)

* Mon Jul  7 2003 Bill Nottingham <notting@redhat.com> 2.4.25-8
- fix leak in module-init-tools-depmod (<arjanv@redhat.com>)
- look in /lib/modules/`uname -r`/updates for modules

* Fri Jun 20 2003 Bill Nottingham <notting@redhat.com> 2.4.25-6
- fix modprobe -C when there is no modules.dep file

* Mon Jun  9 2003 Bill Nottingham <notting@redhat.com> 2.4.25-5
- add IPSEC encryption & auth aliases
- fix alias

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Bill Nottingham <notting@redhat.com> 2.4.25-2
- add joystick alias (#91309)
- add alias for af_key for IPSEC
- update module-init-tools to 0.9.12
- ship a modprobe.conf.dist with the aliases that are built into 2.4
  modutils
- generate a modprobe.conf if needed on install

* Fri Apr 25 2003 Bill Nottingham <notting@redhat.com> 2.4.25-1
- update to 2.4.25
- add floppy alias back (#89097)
- add bluetooth aliases (#88859)

* Tue Apr  3 2003 Bill Nottingham <notting@redhat.com> 2.4.22-10
- quick hack fix for depmod so the installer will work

* Wed Apr  2 2003 Bill Nottingham <notting@redhat.com> 2.4.22-9
- include support for 2.5/2.6 kernels

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 2.4.22-8
- alias block-major-2 off, we never ship it as a module (#71036)

* Mon Feb  3 2003 Bill Nottingham <notting@redhat.com> 2.4.22-7
- make sure we don't use diet anywhere but x86, even if it's lying around
- fix zlib linkage, for real
- switch ftape alias (#7674)

* Fri Jan 31 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for genksyms to not segfault in drivers/char/joystick
  for mainframe kernel builds

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Bill Nottingham <notting@redhat.com> 2.4.22-4
- fix zlib static linkage patch

* Tue Dec 31 2002 Bill Nottingham <notting@redhat.com> 2.4.22-3
- add alias for tun/tap (#80491)

* Mon Dec 30 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add an IBM patch to also load 64bit kernel modules via a 31bit compiled app

* Mon Nov 25 2002 Bill Nottingham <notting@redhat.com> 2.4.22-1
- update to 2.4.22
- don't link zlib dynamically

* Tue Nov 19 2002 Bill Nottingham <notting@redhat.com> 2.4.21-1
- update to 2.4.21
- enable zlib for insmod.static, normal

* Fri Aug 16 2002 Bill Nottingham <notting@redhat.com> 2.4.18-2
- add check for gcc version mismatch between kernel/modules
  (<arjanv@redhat.com>)

* Tue Jul 23 2002 Bill Nottingham <notting@redhat.com> 2.4.18-1
- update to 2.4.18
- add some more default aliases
- fix checking of kernel version

* Mon Jun 24 2002 Bill Nottingham <notting@redhat.com> 2.4.16-1
- update to 2.4.16

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bill Nottingham <notting@redhat.com> 2.4.14-3
- force kallsyms on modules

* Mon Apr  1 2002 Bill Nottingham <notting@redhat.com> 2.4.14-2
- fix support for symbols that contain _R (<streeter@redhat.com>)

* Sat Mar  2 2002 Bill Nottingham <notting@redhat.com> 2.4.14-1
- update to 2.4.14
- take out genksyms.old, no more buildprereq for gperf

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 2.4.13-7/8
- rebuild against diet
- reenable rmmod in the library version, shrink it too

* Wed Feb 27 2002 Bill Nottingham <notting@redhat.com> 2.4.13-5
- rebuild in earlier environments

* Sun Feb 10 2002 Bill Nottingham <notting@redhat.com> 2.4.13-4
- various space shavings in -devel

* Fri Feb  8 2002 Bill Nottingham <notting@redhat.com> 2.4.13-3
- bump rev
- buildprereq gperf

* Mon Feb  4 2002 Bill Nottingham <notting@redhat.com> 2.4.13-1
- update to 2.4.13
- fix GPL symbol export

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com> 2.4.12-9
- shrink insmod.static

* Thu Jan 24 2002 Bill Nottingham <notting@redhat.com> 2.4.12-8
- fix installation of extra libraries (#58427)

* Thu Jan 17 2002 Bill Nottingham <notting@redhat.com> 2.4.12-7
- hack to allow depmod of 64bit kernels on 32bit PPC

* Tue Jan 15 2002 Bill Nottingham <notting@redhat.com> 2.4.12-6
- more ppc64 fixes 

* Thu Jan 10 2002 Bill Nottingham <notting@redhat.com> 2.4.12-5
- fix build on combined 32/64 targets (ppc/sparc)

* Tue Dec 11 2001 Matt Wilson <msw@redhat.com>
- added a -devel subpackage that contains libraries that apps can use
  to implement insmod and rmmod

* Tue Dec  4 2001 Bill Nottingham <notting@redhat.com>
- get rid of some obsolete patches, other tweaks

* Thu Nov 29 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.4.12

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.4.11

* Tue Oct  2 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.10
- deprecate -i, -m arguments to depmod

* Tue Sep 25 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.9

* Wed Aug 29 2001 Bill Nottingham <notting@redhat.com>
- replace modutils-2.4.6-error patch with version that was integrated
  upstream

* Sat Aug 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable char-major-4 for s390/s390x

* Mon Jul  8 2001 Bill Nottingham <notting@redhat.com>
- remove /etc/cron.d/kmod

* Fri Jul  6 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.6
- alias binfmt-0000 off (#9709)
- turn off 'modules.conf is more recent than modules.dep' message (#14276,
  others)
- return nonzero from depmod if there are errors (#40935)
- fix manpage typo (#33123)

* Thu Jul 05 2001 Karsten Hopp <karsten@redhat.de>
- new S390 patch from IBM

* Tue Jun 26 2001 Elliot Lee <sopwith@redhat.com> 2.4.5-3
- Add modutils-2.4.5-stblocal.patch from Jakub. See the e-mail message
  inside the patch file for details.
- Use smp_mflags macro

* Thu Jun 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390/s390x support

* Tue Apr 24 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.5

* Tue Mar  6 2001 Bill Nottingham <notting@redhat.com>
- add default post/preun for binfmt_misc

* Mon Feb 19 2001 Bill Nottingham <notting@redhat.com>
- change ipv6 alias to 'alias net-pf-10 off'

* Tue Feb 13 2001 Bill Nottingham <notting@redhat.com>
- add 'net-pf-10 ipv6' alias (#25405)

* Sun Jan 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change "#ifdef s390" -> "#if defined(__s390__) || defined(__s390x__)"

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.2
- ship a genksyms.old 

* Fri Jan 19 2001 Bill Nottingham <notting@redhat.com>
- fix ppp aliases

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- oops, I blew away other people's changes. Fix that.
- only have tty-ldisc-11 in the aliases once

* Mon Jan  8 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.0
- tweak irda aliases
- remove vixie-cron dependency (it's not *required*)
- add missing %build (where did that go?)

* Sun Jan  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.4.0
- Get rid of obsolete char-major-60==ircom-tty patch
  (moved to 161)

* Sat Jan 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add "ctc{0,1,2} -> ctc" alias for s390
 
* Sat Dec 23 2000 Bill Nottingham <notting@redhat.com>
- add missing comma in alias list
- add irda aliases

* Tue Dec 12 2000 Bill Nottingham <notting@redhat.com>
- add char-major-108 ppp_async alias

* Mon Dec 11 2000 Bill Nottingham <notting@redhat.com>
- fix ide-probe aliases (now ide-probe-mod)

* Wed Nov 22 2000 Matt Wilson <msw@redhat.com>
- 2.3.21, fixes more security problems.

* Thu Nov 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.20, fixes security holes

* Tue Oct 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.19
- add IrDA devices to alias patch
- update source URL

* Thu Oct 26 2000 Bill Nottingham <notting@redhat.com>
- fix ia64 module loading

* Mon Oct  2 2000 Bill Nottingham <notting@redhat.com>
- stupid ia64 tricks

* Fri Sep 29 2000 Jeff Johnson <jbj@redhat.com>
- upgrade to 2.3.17.
- sparc64 ELF hacks.

* Mon Aug 21 2000 Michael K. Johnson <johnsonm@redhat.com>
- Use %{_mandir} for removing kerneld-related man pages.

* Wed Aug  9 2000 Jakub Jelinek <jakub@redhat.com>
- fix build on SPARC

* Tue Aug  8 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.3.14

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- update to 2.3.13
- turn psaux off again
- remove sound patch; it's obsolete

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.12
- fix up ia64

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul  1 2000 Florian La Roche <laroche@redhat.com>
- add aliases for cipcb[0-3]

* Wed Jun 14 2000 Matt Wilson <msw@redhat.com>
- fix build on combined 32/64 bit sparc

* Thu Jun  1 2000 Bill Nottingham <notting@redhat.com>
- modules.confiscation

* Wed May 17 2000 Bill Nottingham <notting@redhat.com>
- add ia64 patch from Intel

* Wed May 17 2000 Jakub Jelinek <jakub@redhat.com>
- fix build with glibc 2.2

* Tue May 09 2000 Doug Ledford <dledford@redhat.com>
- Correct %description to reflect that we don't build kerneld by default

* Fri Apr 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.11

* Mon Apr  3 2000 Bill Nottingham <notting@redhat.com>
- fix net-pf-* aliases for ipx, appletalk

* Fri Mar 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.10

* Thu Feb 17 2000 Matt Wilson <msw@redhat.com>
- added alias for agpgart

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- hardcode psaux alias to off everywhere

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- add a symlink from conf.modules.5 to modules.conf.5

* Fri Jan 29 2000 Bill Nottingham <notting@redhat.com>
- fix breakage *correctly*

* Sat Jan 22 2000 Bill Nottingham <notting@redhat.com>
- fix breakage of our own cause w.r.t sound modules

* Thu Jan 06 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.3.9.
- port RH patches from 2.1.121 to 2.3.9 where needed.
- disable warning about conf.modules for now, in 7.0
  we should move to modules.conf.

* Wed Oct 13 1999 Jakub Jelinek <jakub@redhat.com>
- hardcode psaux alias on sparc to off.

* Tue Oct 05 1999 Bill Nottingham <notting@redhat.com>
- hardcode parport aliases....

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against new glibc in the sparc tree

* Wed Sep 15 1999 Jakub Jelinek <jakub@redhat.com>
- rewrite sparckludge so that separate *64 binaries
  are not needed anymore.

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- apply the last patch in the %%prep section (doh!)

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- add support for the ppp compression modules by default

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- add cron.d file to run rmmod -as

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- take out kerneld

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- add patch to make all raid personalities recognized

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- obsoletes modules
- get rid of the /lib/modules/preferred hack

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- added support for /lib/modules/foo/pcmcia
- make kerneld initscript not start by default

* Tue Feb 23 1999 Matt Wilson <msw@redhat.com>
- added sparc64 support from UltraPenguin

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow it to compile on the arm

* Wed Dec 23 1998 Jeff Johnson <jbj@redhat.com>
- search /lib/modules/preferred before defaults but after specified paths.

* Tue Nov 17 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 2.1.121

* Thu Nov 05 1998 Erik Troan <ewt@redhat.com>
- added -m, -i options

* Thu Oct 01 1998 Michael K. Johnson <johnsonm@redhat.com>
- fix syntax error I introduced when enhancing initscript

* Wed Sep 30 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhance initscript

* Fri Aug 28 1998 Jeff Johnson <jbj@redhat.com>
- recompile statically linked binary for 5.2/sparc

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- pick up ultrapenguin patches (not applied for now).
- pre-generate keyword.c so gperf doesn't have to be present (not applied).
- util/sys_cm.c: fix create_module syscall (signed return on sparc too)

* Wed Jul 15 1998 Jeff Johnson <jbj@redhat.com>
- correct %postun typos

* Fri May 01 1998 Erik Troan <ewt@redhat.com>
- added /lib/modules/preferred to search path

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.1.85
- actually make use of the BuildRoot

* Fri Apr  3 1998 Jakub Jelinek <jj@ultra.linux.cz>
- Fix sparc64, add modinfo64 on sparc.

* Wed Mar 23 1998 Jakub Jelinek <jj@ultra.linux.cz>
- Handle EM_SPARCV9, kludge to support both 32bit and 64bit kernels
  from the same package on sparc/sparc64.

* Fri Nov  7 1997 Michael Fulbright
- removed warning message when conf.modules exists and is a empty

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- patched to honor -k in options
- added modprobe.1
- added init script

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- removed bogus strip of lsmod (which is a script)

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- updated to 2.1.55
- builds in a buildroot

* Mon Aug 25 1997 Erik Troan <ewt@redhat.com>
- added insmod.static

* Sun Aug 24 1997 Erik Troan <ewt@redhat.com>
- built on Intel
- combined rmmod and insmod

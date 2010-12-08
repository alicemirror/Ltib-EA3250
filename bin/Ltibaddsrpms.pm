######################################################################
#
# Copyright © Freescale Semiconductor, Inc. 2004-2007. All rights reserved.
# Copyright (C) Zee2 Ltd, 2009. All rights reserved.
#
# Stuart Hughes, stuarth@freescale.com,  27th March 2007
#
# This file is part of LTIB.
#
# LTIB is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# LTIB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LTIB; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Description:
#
# Additional seldom used addsrpms mode
#
#
######################################################################
package main;

use File::Copy;

sub addsrpms
{
    my ($packages, $srpm, $sn);

    # Use spec name but should really be name:<> in specfile
    foreach my $key (mk_buildlist()) {
         $packages->{$$key->{sn}} = 1;
    }

SRPM:
    for $srpm (@ARGV) {
        warn("skipping: $srpm, doesn't look like an srpm\n"), next
                                               unless $srpm =~ m,\.src\.rpm$,;
        foreach my $fl (`rpm --dbpath $cf->{rpmdb} -qlp $srpm`) {
            $fl =~ m,^([\w-]+)\.spec\s*$, and do { $sn = $1, last }; 
        }
        warn("skipping: $srpm, can't find a spec file\n"),next unless $sn;
        if($packages->{$sn}) {
            warn("$sn is already in LTIB, continue ? y|N\n");
                $_ = <STDIN>;
                warn("skipped $srpm\n"), next unless /^y/i;
        }
        print "importing $srpm to $cf->{rpmdir}\n";
        my ($srpm_name) = $srpm =~  m,/?([^/]+)$,;
        my $cmd = "rpm --dbpath $cf->{rpmdb} "
                . "--define '_topdir $cf->{rpmdir}' -ivh $srpm";
        print "$cmd\n";
        system_nb($cmd) == 0 or die;

        # Fixup the spec file and move to the distro area
        my $specpath = "$cf->{rpmdir}/SPECS/$sn.spec";
        my $tok = parse_spec($specpath, 1) or die();

        if( defined($tok->{pfx}) && $tok->{pfx} =~ m,^/opt/freescale, ) {
            # LTIB spec file do nothing
        } else {
            system_nb("mv $specpath $specpath.bak") == 0 or die();

            # attempt to fix the install destdir
            $tok->{install} =~ s,(\$RPM_BUILD_ROOT\}?),$1/%{pfx}/,gi;

            open(SPEC, ">$specpath") or die("open $specpath : $!");
            print SPEC <<TXT;
%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : $tok->{summary}
Name            : $tok->{name}
Version         : $tok->{version}
Release         : $tok->{release}
License         : ${\( $tok->{license} || "UNKNOWN" )}
Vendor          : ${\( $tok->{vendor}  || "UNKNOWN" )}(LTIB addsrpms)
Packager        : ${\( $tok->{packager}|| "UNKNOWN" )}(LTIB addsrpms)
Group           : $tok->{group}
URL             : ${\( $tok->{url} || "UNKNOWN" )}
$tok->{sources}$tok->{patches}
TXT
            foreach my $url ( split(/\s*\n/, $tok->{sources}), 
                              split(/\s*\n/, $tok->{patches})  ) {
                (undef, $url) = split(/:\s*/, $url, 2);
                my ($fl) = $url =~ m,([^/]+)$,;
                if(-f "$cf->{lpp}/$fl") {
                    warn("$cf->{lpp}/$fl exists, not using srpm copy\n");
                } else {
                    move("$cf->{rpmdir}/SOURCES/$fl", "$cf->{lpp}/$fl")
                                      or warn("move($cf->{rpmdir}/SOURCES/$fl, 
                                                       $cf->{lpp}/$fl) : $!\n");
                }
            }
            print SPEC <<TXT;
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

NOTE: this was imported by ltib -m addsrpms $srpm_name

%Prep
$tok->{prep}
%Build
$tok->{build}
%Install
$tok->{install}
%Clean
rm -rf \$RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
TXT
        }

        # move the spec file to the right place, with checks
        my $specdir = "$cf->{top}/$pcf->{DISTRO}/$sn";
        if(-f "$specdir/$sn.spec" ) {
            print("WARNING: $specdir/$sn.spec exists\n",
                  "renamed: $specdir/$sn-import.spec.orig\n");
            move("$specdir/$sn.spec", "$specdir/$sn.spec.orig");
        }
        mkdir($specdir) unless -d $specdir;
        system_nb("mv $specpath $specdir/$sn.spec") == 0 or die();

        # add an entry into pkg_map
        my $key = 'PKG_' . uc($tok->{name});
        $key =~ s,-,_,g;
        my $pmap = "$cf->{config_dir}/userspace/pkg_map";

        open(PMAP, $pmap) or die("open $pmap : $!\n");
        while(<PMAP>) {
            my ($ckey) = m,^\s*(PKG_\w+)\s* =,;
            next unless $ckey;
            warn("$key already exists in pkg_map, not updating\n"),
                                                    next SRPM if $ckey eq $key;
        }
        close PMAP;
        
        local $^I = '.bak';
        @ARGV = "$cf->{config_dir}/userspace/pkg_map";
        while(<>) {
            s,^(# leave these as the),$key = $tok->{name}\n$1,;
            print;
        }

        # Add an entry to packages.lkc
        my @pkeys = ();
        my $plkc  = "$cf->{config_dir}/userspace/packages.lkc";
        open(PLKC, $plkc) or die("open $plkc : $!\n");
        while(<PLKC>) {
            my ($ckey) = m,\s*config\s(PKG_\w+)\s*$,;
            next unless $ckey;
            warn("$key already exists in packages.lkc, not updating\n"), 
                                                    next SRPM if $ckey eq $key;
            push @pkeys, $ckey;
        }
        close PLKC;

        my $mark = 'PKG_ZLIB';
        foreach my $ckey ( sort @pkeys ) {
            if($key lt $ckey) {
                $mark = $ckey;
                last;
            }
        }
        @ARGV = $plkc;
        while(<>) {
            my ($ckey) = m,\s*config\s(PKG_\w+)\s*$,;
            if($ckey && $ckey eq $mark) {
                print <<TXT;
config $key
    depends CAP_HAS_MMU
    bool "$tok->{name}"
    help
      $tok->{summary}

TXT
            }
            print;
        }
    }
    return 1;
}
1;

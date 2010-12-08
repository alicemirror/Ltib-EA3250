######################################################################
#
# Copyright © Freescale Semiconductor, Inc. 2004-2007. All rights reserved.
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
# Additional functions LTIB uses when making iso releases
#
#
######################################################################
package main;

my $args = {
    fullbsp  => 0,
    warnonly => 0
};

# copy one file and enforce some checks
sub release_copy
{
    my ($url, $ddir, $upps) = @_;
    my ($file) = $url =~ m-/?([^/]+)$-;
    return 1 if -f "$ddir/$file" && -f "$ddir/$file.md5";

    my ($ret, $sav);
    my @sav_list = qw/pp_list_str force_md5get wget_opts quiet/;
    foreach my $k (@sav_list) { $sav->{$k} = $cf->{$k} }
    $cf->{pp_list_str}  = $upps || "gpp_stage cpp_stage";
    $cf->{force_md5get} = 1 unless $args->{warnonly};
    $cf->{quiet}        = 1;
    $cf->{wget_opts}   .= " -q";
    $ret = test_remote_file($url, $cf);
    if($ret || $upps) {
        my $src = get_file($url, $cf, 1) or die("can't get: $url");
        my $cmd = (stat($src))[0] == (stat($ddir))[0] ? "cp -l" : "cp -p";
        foreach my $fl ( $src, $src . '.md5' ) {
            system_nb("$cmd $fl $ddir") == 0 or die;
        }
    } else {
        warn("$url not yet approved for distribution\n");    
        push @{$cf->{missing}}, $url;
        my $ppp = 'ppp';
        if($args->{warnonly} && ! $upps) {
            $ret = release_copy($url, $ddir, $ppp);
        }
    }
    foreach my $k (@sav_list) { $cf->{$k} = $sav->{$k} }; undef $sav;
    return $ret;
}

sub release_copy_pkg
{
    my ($sn, $ddir) = @_;
    return 1 if exists $cf->{rel}{$sn};
    $cf->{rel}{$sn} = 1;
    die("$ddir is not a directory") unless -d $ddir;

    my $msg = "\nchecking: $sn\n";
    $msg .= '=' x length($msg) . "\n";
    my $spec = get_spec($sn);
    warn("specfile: $sn.spec not found, skipping\n"), return unless $spec;
    my $tok = parse_spec($spec) or die();
    $msg .= "License: $tok->{license}";
    my $eula = $tok->{license} =~ m,eula|proprietary,i ? 1 : 0;
    $msg .= " : explicit user acceptance required" if $eula;
    print $msg, "\n";

    # skip non-distributable packages, normally referenced from
    # extra_packages.lkc
    return if $tok->{license} =~ m,No.\s+Distrib,i;

    # copy each source/patch referenced by the package
    my $ret = 1;
    foreach my $url (  split(/\s*\n/, $tok->{sources}),
                       split(/\s*\n/, $tok->{patches})   ) {
        (undef, $url) = split(/:\s*/, $url, 2);
        $ret &= release_copy($url, $ddir) ? 1 : 0;
    }
    push(@{$cf->{eula}}, $tok->{name}) if $eula;
    return $ret;
}

sub release_copy_content
{
    my ($fullbsp, $pkgs, $logfile) = @_;
    my $msg;

    # make a directory to hold the source/package payload
    system_nb("rm -rf $pkgs") == 0 or die;
    mkdir($pkgs) or die("mkdir $pkgs : $!\n");

    # read the toolchains/packages selectable in the platform's 'main.lkc'
    # 20080603, seh: note this is superceeded by the toolchain.lkc file now
    my $lkc = { lkcfile => "$cf->{plat_dir}/main.lkc",
                tcs => 1, bls => 1, kns => 1, };
    find_all_selectable($lkc);

    # find selectable toolchains by correlating the .config and toolchain.lkc
    $lkc->{lkcfile} = "$cf->{config_dir}/userspace/toolchain.lkc";
    $lkc->{config}  = "$cf->{plat_dir}/.config";
    tc_lookup_selectable($lkc);
    
    print <<TXT;

${\( $args->{warnonly} ? "*** TEST RELEASE, NOT TO DISTRIBUTED EXTERNALLY ***" : "" ) }

Checking licensing and external availabity of sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following constraints/checks are enforced:

1/ All source/patches in the default configuration must be distributable.

2/ Any sources/patches not in the default configuration that are not
distributable are not be copied to the ISO image.

3/ Any content copied to the ISO image has it's md5 checksum verified by
downloading a fresh copy of the md5sum file and using it to verify the
content it checksums.

4/ Files already present on local disk in the LPP will be used.  Any
missing files will be downloaded from either the GPP staging area
or the CPP (Clickthru) staging area.

                  ------------------------
TXT

    $msg  = "\n\nCopying content from default configuration (mandatory)\n";
    $msg .= '-' x length($msg) . "\n\n";
    print $msg;
    $msg  = "checking: toolchain\n";
    $msg .= '=' x length($msg) . "\n";
    print $msg;
    my ($rpm, $srpm);
    $rpm = tc_name($pcf->{TOOLCHAIN});
    ($srpm = $pcf->{TOOLCHAIN}) =~ s,\.i\d86\.rpm,.src.rpm,;
    release_copy($rpm, $pkgs)  || $args->{warnonly}
                               or die "Error: $rpm  required by defconfig\n";
    release_copy($srpm, $pkgs) || $args->{warnonly}
                               or die "Error: $srpm required by defconfig\n";
    foreach my $key (mk_buildlist()) {
        next unless $$key->{en};
        
        release_copy_pkg($$key->{sn}, $pkgs) || $args->{warnonly}
                                  or die "Error: required by default config\n";
    }
    $msg  = "\n\nCopying additional packages in host config (mandatory)\n";
    $msg .= '-' x length($msg) . "\n\n";
    print $msg;
    release_copy_pkg('rpm-fs', $pkgs) || $args->{warnonly}
                              or die "Error: required by host support config\n";
    pkg_cache_init();
    my $opcf = $pcf;
    my $opd  = $cf->{plat_dir};
    $cf->{plat_dir} = "config/platform/host";
    $pcf = parse_dotconfig($cf->{hostconfig});
    foreach my $key (mk_buildlist()) {
        next unless $$key->{en};
        release_copy_pkg($$key->{sn}, $pkgs) || $args->{warnonly}
                              or die "Error: required by host support config\n";
    }
    pkg_cache_init();
    $pcf = $opcf;
    $cf->{plat_dir} = $opd;

    # finish here unless you want everything that is potentially selectable
    return 1 unless $fullbsp;

    $msg  = "\n\nCopying additional selectable content (optional)\n";
    $msg .= '-' x length($msg) . "\n\n";
    print $msg;
    $msg  = "\nchecking for additional toolchains\n";
    $msg .= '-' x length($msg) . "\n";
    print $msg;
    foreach my $k (keys %{$lkc->{toolchains}}) {
        $rpm = tc_name($k);
        ($srpm = $k) =~ s,\.i\d86\.rpm,.src.rpm,;
        release_copy($rpm, $pkgs);
        release_copy($srpm, $pkgs);
    }
    foreach my $k ( qw/bootloaders kernels/ ) {
        $msg  = "\nChecking for additional $k\n";
        $msg .= '-' x length($msg) . "\n";
        print $msg;
        foreach my $p (keys %{$lkc->{$k}}) {
            release_copy_pkg($p, $pkgs);
        } 
    }

    $msg  = "\nChecking for additional packages\n";
    $msg .= '-' x length($msg) . "\n";
    print $msg;
    foreach my $key (mk_buildlist()) {
        next if $$key->{en};
        release_copy_pkg($$key->{sn}, $pkgs);
    }
    return 1;
}

sub release_main
{
    $args = { %$args, @_ };
    local $_;
    my $logfile  = 'RELEASE_COPY_CONTENT';
    my $gitree   = -d "$cf->{top}/.git";

    # For now, don't allow batch mode releases until we've figured out
    # all the details of passing in the information needed.
    die("Batch mode is enabled, cannot make iso release!!\n") if $cf->{batch};

    # reset the path to original so we can callout to ltib as we were called
    $ENV{PATH} = $cf->{path_orig};

    print <<TXT;

You are about to create an iso image from this working project.
This will include all sources and built rpms for the target platform,
as well as the LTIB source code.

${\( $args->{warnonly} ? "*** TEST RELEASE, NOT TO BE DISTRIBUTED EXTERNALLY ***" : "" ) }

Before doing this, you should have done the following:

 1. Make sure you have committed any changes
 2. Make sure your source code is up to date
 3. Configured ltib for the target
 4. Run ltib to build all the selected packages

Do you want to continue: Y|n ?
TXT
    if(! $cf->{batch} ) {
        $_ = <STDIN>;
        print("aborted\n"), return 1 if /^n/;
    }

    # Normally everything is driven from the SCM but there are some secret
    # tagnames that let you do releases from working copies, or just 
    # the HEAD of the SCM (or the top of the branch you're on).
    # HEAD : normal, except no tagging use the trunk HEAD or top of branch
    # localdir : use the content of the local dir using a list in file MANIFEST
    # localdir_nobuild : same as localdir, but don't do the package build
    my ($plat) = $cf->{plat_dir} =~ m,([^/]+)$,;
    my $tag = "rel-$plat-$cf->{stime}";
    my $date = gm_yyyymmdd();
    my $nogo = $args->{warnonly} ? 'non-distributable-' : '';
    my $rel = $nogo . "ltib-$plat-$date";
    print "Please enter the tag name for this release\n",
          "Giving the name 'HEAD' will use the head of the trunk, or ",
          "current branch.\n";
    if($args->{warnonly} || $gitree) {
        print("In test mode, only existing tags can be used (e.g use HEAD)\n");
    } else {
        print("If you type enter, the timestamp $tag will be used.\n");
    }
    if(! $cf->{batch} ) {
        while(1) {
            $_ = <STDIN>;
            if ( !defined $_ ) {
                # Prevent infinite loop if tag is from here file in script.
                die("STDIN is not defined, exiting\n");
            }
            chomp($_);
            $tag = $_ if $_;
            last if $tag eq 'localdir' || $tag eq 'localdir_nobuild' 
                                       || $tag eq 'HEAD';
            if(! $gitree && $tag !~ m,^[a-zA-Z][\w-]+$,) {
                warn(<<TXT);

Illegal tag name, tags need to be specified as follows:

* Start with an uppercase or lowercase letter
* Subsequently and can also contain uppercase and lowercase letters, 
  digits, `-', and `_'
TXT
                next;
            }

            print("gathering a list of existing remote tags, pls wait:\n");
            my $scmtags = get_scm_tags();
            if($args->{warnonly} || $gitree) {
                last if exists $scmtags->{$tag};
                print(  "\tThe tag you've does not exist, ",
                                                    "please choose another\n");
            } else {
                last unless exists $scmtags->{$tag};
                print(  "The tag you've chosen is already in use, ",
                                                    "please choose another\n");
            }
        }
    }

    # check for unsaved config changes
    print "\nChecking for unsaved config changes:\n";
    my @devs = glob("$cf->{plat_dir}/*.dev");
    system_nb(<<TXT);
set -e
diff -qN  $cf->{plat_dir}/defconfig $cf->{plat_dir}/.config
for i in @devs
do
    diff -qN $cf->{plat_dir}/`basename \$i .dev` \$i
done
TXT
    if($? != 0) {
        warn "\tPlease save your changes before continuing\n";
        die unless $args->{warnonly};
    }
    if($tag ne 'localdir' && $tag ne 'localdir_nobuild') {
        print "Checking that the source tree is up to date:\n";
        if( ! src_tree_is_clean() ) {
            warn("\tYour source tree has got modifications, ",
                                                "please commit these first.\n");
            die if ! $args->{warnonly} || $gitree;
        }
        if( ! check_scm_id_is_remote($tag)  ) {
            warn("\tThe tag you are gave does not exist in ",
                                                  "the upstream repository.\n");
            die if ! $args->{warnonly};
        }

    }

    # turn on logging
    redirect("| tee $logfile");

    # avoid uninitialized warning
    @{$cf->{missing}} = ();
    @{$cf->{eula}}    = ();

    # copy all the package contents first
    release_copy_content($args->{fullbsp}, 'pkgs', $logfile);

    # turn off logging
    redirect();

    if($args->{warnonly} == 0 && $tag ne 'HEAD' && $tag ne 'localdir'
                              && $tag ne 'localdir_nobuild') {
        tag_repository($tag) or die;
    }
    my $etag = $tag;
    if($etag eq 'HEAD' && (my $branch = get_scm_branch())) {
        $etag = $branch;
    }
    system_nb('rm -rf stage') if -d 'stage';
    if($tag ne 'localdir' && $tag ne 'localdir_nobuild') {
        print("exporting repository using tag: $etag\n");
        export_repository($etag, 'stage') or die;
    }

    system_nb(<<TXT) ==  0 or die;
set -x -e

if [ "$tag" != "localdir" -a "$tag" != "localdir_nobuild" ]
then
    for i in `ls stage/config/platform | grep -E -v '($plat|host)'`
    do
        rm -rf stage/config/platform/\$i
    done
    rm -rf stage/dist/FC-2
    rm -rf stage/internal
    rm -rf $rel
else
    mkdir stage
    rsync -av --files-from=MANIFEST . stage
    if [ -d overlay -a -f overlay/MANIFEST ]
    then
        rsync -av --files-from=overlay/MANIFEST overlay stage
    fi
fi
mkdir $rel
mv stage $rel
mv $rel/stage $rel/$rel
cp $rel/$rel/bin/ltib_install $rel/install

# work in the release staging area
cd $rel/$rel

# Remove internal additional packages
echo "comment 'Additional Package selection'" > config/userspace/extra_packages.lkc

# built to make sure all generated pieces make it onto the iso
if [  "$tag" = "localdir_nobuild" ]
then 
    ./ltib --preconfig $cf->{plat_dir} -m config --batch
else
    ./ltib --preconfig $cf->{plat_dir} --configure --batch
fi

# copy the pre-built images if any to the iso so usable without ltib
mkdir ../images
set +e
cp -a rootfs*gz* ../images/
cp -a rootfs/boot ../images/
set -e

# remove the rootfs components
if [  "$tag" != "localdir_nobuild" ]
then 
    ./ltib -m clean
fi

# remove unwanted log files and host package install check files
rm -f .host_wait_warning* host_config.log .tc_test* .lock_file
rm -f $cf->{rpmdb_nfs_warning}
rm -rf rpm/BUILD/*
rm -rf rootfs.tmp

cd -

TXT
    if($args->{warnonly} == 0) {
        # Disable internal Freescale features
        my $o_irs = $/;
        $/ = undef;
        open(F, "+<$rel/$rel/config/userspace/defaults.lkc") or die "open:  $!";
        $_ = <F>;
        s,(config\s+CAP_FSL_INT\s+bool\s+default\s+)y,$1n,m;
        seek(F, 0, 0)                              or die "seek:  $!";
        print F                                    or die "print: $!";
        truncate(F, tell(F))                       or die "trunk: $!";
        close(F)                                   or die "close: $!";
    
        open(F, "+<$rel/$rel/.ltibrc") or die "open: $!";
        $_ = <F>;
        s,#?http://(10|wwwgate|auslx).*\n,,mg;
        s,(%gpp_proxy\s*)1,${1}0,msg;
        seek(F, 0, 0)                              or die "seek:  $!";
        print F                                    or die "print: $!";
        truncate(F, tell(F))                       or die "trunk: $!";
        close(F)                                   or die "close: $!";
        $/ = $o_irs;
    }

    # output some helpful release information (overwrite)
    my $ext_tag = $tag . " (" . get_scm_tag() . ")";
    write_release_info("$rel/$rel/RELEASE_INFO", $ext_tag, $rel) or die;

    system_nb(<<TXT) ==  0 or die;
set -x -e
if [ -d pkgs ] 
then
    mv pkgs $rel
fi
mkdir $rel/release_logs $rel/$rel/release_logs
for i in $logfile $rel/$rel/RELEASE_INFO
do
    cp \$i $rel/release_logs/
    mv \$i $rel/$rel/release_logs/
done
if [ -d addons ]
then
    cp -a addons/* $rel
fi
cd $rel
tar --exclude rootfs -zcvf ltib.tar.gz $rel
cd -
cd $rel/$rel
./ltib -m distclean --batch
cd -
cd $rel
rm -rf $rel
cd -
if mkisofs -help 2>&1 | grep -q joliet-long
then
    mkisofs -A "$rel" -J -allow-leading-dots -l -publisher "Freescale" -o $rel.iso -r -v -V "ltib" -joliet-long $rel
else
    mkisofs -A "$rel" -L -l -P "Freescale" -o $rel.iso -r -v -V "ltib" $rel
fi
rm -rf $rel

TXT

    if( @{$cf->{missing}} ) {
        my $not = $args->{warnonly} ? '' : 'not';
        warn "\n\n",
             "The following files that are not distributable\n",
             "were $not included in the iso image:\n\t",
             join("\n\t", @{$cf->{missing}}), "\n\n";
    }
    if( @{$cf->{eula}} ) {
        warn "\n\n",
             "The following packages require acceptance",
             " of an End User License Agreement:\n\t",
             join("\n\t", @{$cf->{eula}}), "\n\n";
    }
    return 1;
}

sub find_all_selectable
{
    my ($hr) = @_;
    my $lkc  = $hr->{lkcfile} or die;
    my $scan = '';
    local $_;

    open(LKC, $lkc) or die("open $lkc : $!");
    while(<LKC>) {
        $scan = ''   if m,^\s*$,;
        $scan = ''   if m,^\s*config\s,;
        $scan = 'tc' if m,^\s*config\s+TOOLCHAIN$,;
        $scan = 'bl' if m,^\s*config\s+PKG_U_BOOT$,;
        $scan = 'kn' if m,^\s*config\s+PKG_KERNEL$,;

        if($hr->{tcs} && $scan eq 'tc' && m,^\s*default\s+"?([^\s"]+\.rpm),){
            $hr->{toolchains}{$1} = 1;
            next;
        }
        if($hr->{bls} && $scan eq 'bl' && m,^\s*default\s+"?([^\s"]+),){
            $hr->{bootloaders}{$1} = 1;
            next;
        }
        if($hr->{kns} && $scan eq 'kn' && m,^\s*default\s+"?([^\s"]+),){
            $hr->{kernels}{$1} = 1;
            next;
        }
    }
    close LKC;
    #while(my($k,$v) = each %$hr) { print "$k: ", join(', ', keys %$v), "\n" }
    return 1;
}

sub tc_lookup_selectable
{
    my ($hr) = @_;
    $path = $hr->{config};
    open(FN, $path) or die "open $path : $!";
    @cf = <FN>;
    close(FN);
    foreach my $ln (@cf) {
        if($ln =~ m,^# CONFIG_(TOOLCHAIN[\S]+)\s+is not set,) {
            $tc = correlate_tc_key($hr->{lkcfile}, $1);
            $hr->{toolchains}{$tc} = 1 if $tc;
        }
    }
}

sub correlate_tc_key
{
    my ($path, $key) = @_;
    open(FN, $path) or die "open $path : $!";
    $on = 0;
    while(<FN>) {
        m,config\s+TOOLCHAIN\s*$, and do  { $on = 1; next };
        if($on) {
            m,^\s*$,              and do  { $on = 0; next };
            m,^\s*default\s+"?([^\s"]+\.rpm)\s+.+$key, and do { return $1 };
        }
    }
    return;
}

1;

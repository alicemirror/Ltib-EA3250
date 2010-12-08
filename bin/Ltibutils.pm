######################################################################
#
# Copyright © Freescale Semiconductor, Inc. 2004-2007. All rights reserved.
#
# Stuart Hughes, stuarth@freescale.com,  22nd Feb 2005
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
# Utility functions loaded by LTIB
#
#
######################################################################
package Ltibutils;
require 5.003;
require Exporter;

use File::Find;
use File::Basename;
use Fcntl qw(:DEFAULT :flock :mode);

# Test for optional modules
BEGIN {
    $have_md5 = 0;
    if( eval "require Digest::MD5" ) {
        Digest::MD5->import();
        $have_md5 = 1;
    } else {
        warn("Don't have Digest::MD5, will fallback to md5sum\n");
    }
    $have_request_common = 0;
    if( eval "require HTTP::Request::Common" ) {
        HTTP::Request::Common->import(HEAD);
        $have_request_common = 1;
    } else {
        warn("Don't have HTTP::Request::Common\n");
    }
    $have_useragent = 0;
    if(eval "require LWP::UserAgent") {
        $have_useragent = 1;
    } else {
        warn("Don't have LWP::UserAgent\n");
    }
    warn( "Cannot test proxies, or remote file availability without both\n"
         ."HTTP::Request::Common and LWP::UserAgent\n")
                               unless $have_request_common && $have_useragent;
}

use strict 'vars';
use vars qw(@ISA @EXPORT $have_request_common $have_useragent $have_md5
                         $proxy_tested $pp_list_str $app_checks $verbose
                         $hl $cf);
@ISA = qw(Exporter);
@EXPORT = qw( parse_dotconfig gm_yyyymmdd parse_config
             parse_spec get_file touch g2larch
             get_ver cmp_ver mk_uboot_kernel mk_fs_image
             cmd_w_to system_nb caller_stack test_remote_file 
             md5sum write_file write_config try_lock_file release_lock_file
             src_tree_is_clean export_repository get_scm_tags tag_repository
             get_scm_tag get_scm_branch check_scm_id_is_remote);

# import verbose, cf from the main package
*verbose = \$main::verbose;
*cf      = \$main::cf;

my $scmtags = {};

sub parse_dotconfig
{
    my($f) = @_;
    my $hr = {};
    warn("parsing $f\n") if $verbose;
    open(my $fh, $f) or warn("parse_dotconfig: line ",  (caller())[2],
                           ", open $f: $!\n"), return;
    while(<$fh>) {
        chomp;
        my ($k, $v) = m,(CONFIG_[^\s=]+)[\s=]+(.*),;
        next unless $k;
        $k =~ s,\bCONFIG_,,;
        $v =~ s,is not set,,;
        # strip off the enclosing quotes
        $v =~ s,^",,;
        $v =~ s,"$,,;
        $hr->{$k} = $v;
    }
    close $fh;
    while($verbose && (my($k,$v) = each %$hr)) { warn "$k=$v\n" };
    return $hr;
}

#
# gm_yyyymmdd can return the date, either in GMT, or in localtime.
# Usefull when the local timezone is far away from GMT.
sub gm_yyyymmdd
{
    if ($cf->{use_localtime}) {
        my ($day, $month, $year) = (localtime)[3,4,5];
        return sprintf("%04d%02d%02d", $year+1900, $month+1, $day);
    } else {
        my ($day, $month, $year) = (gmtime)[3,4,5];
        return sprintf("%04d%02d%02d", $year+1900, $month+1, $day);
    }
}

sub parse_config
{
    my $args = { fn             => '',
                 strip_blank    => 1,
                 strip_comment  => 1,
                 strip_trailing => 1,
                 @_ };

    my ($hr, $tok, $tok_name, $ld, $fh) = ({}, "", "", 0);
    local $_;
    open($fh, $args->{fn}) or warn("open $args->{fn}: $!"), return;
    while(<$fh>) {
        if( eof || /^%([\w-]+)/ ) {
            if( $ld ) {
                $tok .= $_ if eof;
                $tok =~ s/\s*$//;
                $hr->{$tok_name} = $tok;
                $ld = 0;
            }
            $tok_name = $1;
            $ld       = 1;
            $tok      = "";
        } else {
            $tok .= $_ if $ld;
        }
    }
    close $fh;

    for $tok ( keys %$hr ) {
        next unless defined $hr->{$tok};
        if($args->{strip_comment}) {
            $hr->{$tok} =~ s,^\s*#.*\n?,,gm;
        }
        if($args->{strip_blank}) {
            $hr->{$tok} =~ s,^\s*\n,,gm;
        }
        if($args->{strip_trailing}) {
            $hr->{$tok} =~ s,\s+$,,gm;
        }
    }
    while($verbose && (my($k,$v) = each %$hr)) { warn "$k=$v\n" };
    return $hr;
}

sub write_config
{
    my ($fn, $hr) = @_;
    my $buf = "# Auto-generated by ltib on ${\( scalar(gmtime()) )} UTC\n\n";
    foreach my $k ( sort keys %$hr) {
        $buf .= '%' . "$k\n$hr->{$k}\n\n";
    }
    return write_file($fn, $buf);
}


sub parse_spec
{
    my ($specname, $no_reduce, $mode) = @_;
    my $tokens   = { 
                     sources => '',
                     patches => '',
                     prep    => '',
                   };
    my $defines  = {};
    $no_reduce ||= 0;
    $mode ||= '';

    # Read in the whole file in one go. Okay as spec files are small
    local $/ = undef;
    open(SPEC, $specname) or warn("can't open $specname : $!"), return;
    local $_ = <SPEC>;
    close SPEC;

    # match and extract defines/tokens
    m,^name\s*:\s*([\S]+),mi       and do { $tokens->{name} = $1 };
    warn("$specname  does not contain an entry for Name:"), return
                                                         unless $tokens->{name};
    return $tokens if $mode eq 'name';
    m,^%define\s+base\s+(.+),m and do { $tokens->{base}  = $1 };
    m,^%define\s+pfx\s+([\S]+),m and do { $tokens->{pfx}  = $1 };
    m,^%define\s+buildsubdir\s+([\S]+)$,m 
                                and do { $tokens->{pkg_dir_name} = $1 };
    m,^summary\s*:\s*(.+)$,mi   and do { $tokens->{summary} = $1 };
    m,^version\s*:\s*([\S]+),mi    and do { $tokens->{version} = $1 };
    m,^release\s*:\s*([\S]+),mi    and do { $tokens->{release} = $1 };
    m,^license\s*:\s*(.+)$,mi   and do { $tokens->{license} = $1 };
    m,^vendor\s*:\s*(.+)$,mi   and do { $tokens->{vendor} = $1 };
    m,^packager\s*:\s*(.+)$,mi   and do { $tokens->{packager} = $1 };
    m,^group\s*:\s*(.+)$,mi   and do { $tokens->{group} = $1 };
    m,^url\s*:\s*(.+)$,mi   and do { $tokens->{url} = $1 };
    while(m,^(source\d*\s*:\s*.+)$,mig) { $tokens->{sources} .= "$1\n" };
    while(m,^(patch\d*\s*:\s*.+)$,mig ) { $tokens->{patches} .= "$1\n" };
    m,^buildroot\s*:\s*(.+),mi  and do { $tokens->{buildroot} = $1 };
    m,^prefix\s*:\s*(.+),mi  and do { $tokens->{prefix} = $1 };
    m,^%setup\s+.*-n\s+(.+)$,mi   and do { $tokens->{pkg_dir_name} = $1 };
    m,^%prep(\s*.+?)(?:(^%build)|\Z),msi and do { $tokens->{prep} = $1 };
    m,^%build\s*(.+?)(?:^%install),msi  and do { $tokens->{build} = $1 };
    m,^%install\s(.+?)(?:^%clean),msi and do { $tokens->{install} = $1 };
    m,^%files(\s*.+?)(?:(^\s*$)|\Z),msi and do { $tokens->{files} = $1 };

    # derive the directory name the package will build into
    $tokens->{pkg_dir_name} ||= "$tokens->{name}-$tokens->{version}";

    # We need to reduce at least the name, version, release into
    # absolute terms so that we can run 'listpkgs' and also
    # list all the sources/patches unambiguously
    $defines->{$1} = $2 while m,^%define\s+([^\s]+)\s+([^\s]+)$,gm;
    interp_vars($defines, $tokens, qw/name version release/);
    foreach my $k (qw/name version release/) {
        $defines->{$k} = $tokens->{$k};
    }
    interp_vars($defines, $tokens, qw/sources patches pkg_dir_name/); 

    while($verbose && (my($k,$v) = each %$tokens)) { warn "$k=$v\n" };
    return $tokens;
}

sub interp_vars
{
    my ($defs, $hr, @list) = @_;
    local ($_, $1);
    foreach (@list) {
        while( $hr->{$_} =~ m,(%{?([^}]+)}?),g ) {
            my $rep = '';
            if( defined $defs->{$2} ) {
                $rep = $defs->{$2};
            } else {
                warn("dropping $1 in spec token: $_\n");
            }
            $hr->{$_} =~ s,\Q$1\E,$rep,;
        }
    }
}

sub get_file
{
    my ($url, $cf, $force_md5) = @_;
    warn("no url passed"), return unless $url;
    warn("lpp: $cf->{lpp} is not a directory"), return unless -d $cf->{lpp};
    my ($path,  $refmd5);
    my ($file)  = $url =~ m-/?([^/]+)$-;

    # This is needed to let LWP::UserAgent cycle through the authentication
    # types in the test proxy section (called from here lower down)
    local $SIG{__DIE__} = 'DEFAULT';

    # only test the file if in test mode
    return test_remote_file($url, $cf) if $cf->{dltest};

    # Don't check md5sums if file is local unless forced.  The rationale is
    # that it would be checked when downloaded, and if not downloaded, we
    # may not want to do network accesses.
    my @ldirs = grep { ! m,^\s*$, && ! m,\s*#, } split(/\s+/, $cf->{ldirs});
    my @sdirs = ($cf->{lpp}, @ldirs, "$cf->{top}/pkgs");
    foreach my $dir ( @sdirs ) {
        $path = "$dir/$file";
        if(-f $path) {
            return $path if ! $force_md5 || $cf->{dry};

            # try to get the reference md5sum for this file
            $refmd5 = get_ref_md5($file, $cf, $dir);
            return md5sum_ok($path, $refmd5) ? $path : undef;
        }
    }
    print("get_remote_file: $url\n"), return if $cf->{dry};

    # try to get the reference md5sum for this file
    $refmd5 = get_ref_md5($file, $cf, $cf->{lpp}) unless $refmd5;

    # try to get the file from various remote locations
    $path = get_remote_file($url, $cf) or return;

    # if we got the file, verify the md5sum
    return md5sum_ok($path, $refmd5) ? $path : undef;
}

$proxy_tested = 0;
sub test_proxy
{
    my ($cf) = @_;

    return if $proxy_tested;
    $proxy_tested = 1;

    return if $cf->{bypass_network_tests};
    return unless $have_request_common && $have_useragent;

    my ($res, $req, $px_name);
    my $ua = LWP::UserAgent->new;
    my $no_proxies = "No http or ftp proxy has been set, proxies forced off\n";
    foreach my $pp ( @{$cf->{pp_list}} ) {
        $px_name = $pp . '_proxy';
        next unless $cf->{$px_name};
        if(!$cf->{http_proxy}) {
            warn($no_proxies) if $no_proxies;
            $no_proxies = '';
            $cf->{$px_name} = 0;
            next;
        }
        print "Testing proxy connection for \U$pp\E : ";
        $req = HEAD($cf->{$pp . '_url'});
        $ua->proxy('http', $cf->{http_proxy});
        local $SIG{ALRM} = sub { die "timeout" };
        eval {
            alarm(8);
            $res = $ua->request($req);
            alarm(0);
        };
        print("OKAY\n"), next if $res->is_success;
        warn("FAIL\n");
        if($@) {
            warn("error: $@\n");
        } else {
            warn("response was: ", $res->status_line, "\n");
        }
        warn("Can't get $pp index, proxy forced off\n");
        $cf->{$px_name} = 0;
    }
    return 1;
}

# before calling this you need to have validated the proxies and the pp_list
sub test_remote
{
    my ($cf, $pp, $file) = @_;
    $file ||= '';
    return unless $cf->{$pp . '_url'};

    my $ua  = LWP::UserAgent->new;
    my $req = HEAD($cf->{$pp . '_url'} . $file);
    $ua->proxy('http', $cf->{http_proxy}) if $cf->{$pp . '_proxy'};
    my $res = $ua->request($req);
    if($res->is_success) {
        # bitshrine redirects on error and returns OK 200, this is a hack
        return if $res->base =~ m,bad_request.html$,;
        print("OK \U$pp\E: ", $file ? $file : "is available", "\n");
        return 1;
    }
    return;
}

$pp_list_str = '';
sub test_pp_list
{
    my ($cf) = @_;
    return scalar @{$cf->{pp_list}} if $cf->{pp_list_str} eq $pp_list_str;
    $pp_list_str = $cf->{pp_list_str};
    return 1 if $cf->{bypass_network_tests};
    return 1 unless $have_request_common && $have_useragent;


    # test the proxy connection
    test_proxy($cf);

    # test and validate each package pool connection
    my $pp_list = [];
    foreach my $pp ( split(/\s+/, $cf->{pp_list_str}) ) {
        if(exists $cf->{$pp . '_ava'}) {
            push(@$pp_list, $pp) if $cf->{$pp . '_ava'}; 
        } else {
            $cf->{$pp . '_ava'} = 0, next unless $cf->{$pp . '_url'};
            print("Testing network connectivity for $pp\n");
            $cf->{$pp . '_ava'} = test_remote($cf, $pp);
            push(@$pp_list, $pp) if $cf->{$pp . '_ava'}; 
        }
    }
    $cf->{pp_list} = $pp_list;
    warn "updated pp_list=@{$cf->{pp_list}}\n" if $verbose;
    my $ret = scalar @{$cf->{pp_list}};
    return $ret;
}

sub test_remote_file
{
    die "Some modules to test remote file access are missing"
                               unless $have_request_common && $have_useragent;
    my ($url, $cf) = @_;
    warn("no url passed"), return unless $url;
    my ($file) = $url =~ m-/?([^/]+)$-;
    my $ua  = LWP::UserAgent->new;
    my ($req, $res);

    # test the ppp/gpp connection
    test_pp_list($cf) or return;

    foreach my $pp ( @{$cf->{pp_list}}  ) {
        return 1 if test_remote($cf, $pp, $file);
    }
    print("FAILED ", join(" ", @{$cf->{pp_list}}), ": $file\n");
    return;
}

sub get_remote
{
    my($dest, $pxys, $wget_opts, $pxmode, $url) = @_;
    return system_nb(<<TXT) == 0;
cd $dest
$pxys wget $wget_opts --proxy=$pxmode $url 2>&1
cd - >/dev/null
TXT
}

sub get_remote_file
{
    my ($url, $cf, $dest) = @_;
    return test_remote_file($url, $cf) if $cf->{dry};
    warn("no url passed"), return unless $url;
    $dest ||= $cf->{lpp};
    warn("dest (lpp): $dest is not a directory"), return unless -d $dest;
    my ($file)  = $url =~ m-/?([^/]+)$-;
    my $path = "$dest/$file";

    # test the ppp/gpp connection
    test_pp_list($cf) or return;

    foreach my $pp ( @{$cf->{pp_list}}  ) {
        next unless $cf->{$pp . '_url'};
        print "Try $file from the \U$pp\E\n" unless $cf->{quiet};
        my $pxys   = $cf->{$pp . '_proxy'} ? 'http_proxy=' . $cf->{http_proxy}
                                           : '';
        my $pxmode = $cf->{$pp . '_proxy'} ? 'on' : 'off';
        my $rpath  = $cf->{$pp . '_url'} . "/$file";
        get_remote($dest, $pxys, $cf->{wget_opts}, $pxmode, $rpath);
        return $path if -f $path;
    }
    return;
}

sub get_ref_md5
{
    my($file, $cf, @dirs) = @_;
    my ($refmd5, $md5, $fn);
    my $md5name = "$file.md5";
    my $md5path = "";

    # look for and check local files first
    foreach my $dir ( @dirs ) {
        if(-f "$dir/$md5name") {
            if($cf->{force_md5get}) {
                unlink "$dir/$md5name";
                next;
            }
            $md5path = "$dir/$md5name";
            last;
        }
    }
    $md5path = get_remote_file($md5name, $cf) unless $md5path;
    return unless $md5path;
    return if $cf->{dry};

    # if the md5 file exists, look for the file's md5sum in there
    open(MD5, $md5path) or warn("open $md5path: $!"), return;
    while(<MD5>) {
        ($md5, $fn) = split(/\s+/);
        if(defined $fn &&  $fn eq $file) {
            $refmd5 = $md5;
            last;
        }
    }
    close MD5;
    if(! $refmd5 ) {
        unlink("$md5path.bad");
        rename($md5path, "$md5path.bad");
        warn("Error: corrupt md5 file: $md5path, renamed to $md5path.bad\n");
        return;
    }
    return $refmd5;
}

sub md5sum_ok
{
    my ($path, $refmd5) = @_;
    if(! $refmd5) {
        warn "WARN: skipping md5sum check for $path, md5 file was not found\n";
        return 1;
    }
    if(md5sum($path) eq $refmd5) {
        warn "OKAY: md5sum($path)\n" if $verbose;
        return 1;
    }
    warn "ERROR: md5sum mismatch, re-naming $path to $path.bad, ",
         "please re-try\n";
    rename($path, "$path.bad");
    return;
}

sub md5sum
{
    my ($path) = @_;
    if(! $have_md5 ) {
        my ($md5) = split(/\s+/, `md5sum $path`);
        return $md5;
    }
    open(F, $path) or warn("can't open $path: $!"), return;
    binmode(F);
    return Digest::MD5->new->addfile(*F)->hexdigest;
}


sub touch
{
    return system_nb("touch @_") == 0;
}

sub g2larch
{
    my ($gnuarch) = @_;
    return unless $gnuarch;
    my $arches = {
        powerpc => "ppc",
    };
    if( exists($arches->{$gnuarch}) ) {
        return $arches->{$gnuarch};
    }
    return $gnuarch;
}

sub cmp_ver
{
    my @ver = split(/\./, $_[0]);
    my @min = split(/\./, $_[1]);
    my $res;

    for my $ref (@ver) {
        if($ref =~ m,[\D], || $min[0] =~ m,[\D],) {
            $res = $ref cmp $min[0];
        } else  {
            $res = $ref <=> $min[0];
        }
        warn "ref=$ref, min=$min[0]\n" if $verbose;
        return $res if $res != 0;
        shift(@min);
        last unless $min[0];
    }
    return 0;
}


$app_checks = {
    binutils         => 'ar --version 2>/dev/null',
    'gcc-c++'        => 'g++ --version 2>/dev/null',
    glibc            => 'ldd --version 2>/dev/null',
    'glibc-devel'    => sub { -f '/usr/lib/libm.so' || -f '/usr/lib64/libz.so'},
    'glibc-headers'  => sub { -f '/usr/include/stdio.h' },
    'libstdc++' => sub {
            return system_nb(<<TXT) == 0;
echo '#include <iostream>
int main() { std::cout << "test"; }' | g++ -x c++ - -o /dev/null
TXT
                       },
    lkc              => 'mconf -h 2>/dev/null',
    ncurses          => 'tic -V 2>/dev/null',
    'ncurses-devel'  => sub { -f '/usr/include/ncurses.h' },
    'rpm-build'      => sub { `rpmbuild --version 2>/dev/null` },
    sudo             => 'sudo -V 2>/dev/null',
    tcl              => "echo 'puts \$tcl_patchLevel' | tclsh",
    texinfo          => sub {
                       warn  "WARNING: you may also need to install:"
                            ." tetex-fonts, dialog and textex\n"
                         unless  -f '/usr/share/texmf/tex/texinfo/texinfo.tex';
                        `makeinfo --version 2>/dev/null`;
                    },
    zlib         => sub { my @f = (glob('/usr/lib/libz.so*'),
                                   glob('/lib/libz.so*'),
                                   glob('/lib64/libz.so*')  ); @f > 1 ? 1 : 0 },
    'zlib-devel' => sub { -f '/usr/include/zlib.h' },
};

sub get_ver
{
    my ($pkg) = @_;
    local $_;

    if( ! defined($app_checks->{$pkg}) ) {
        $_ = `$pkg --version 2>/dev/null`;
    } elsif(ref($app_checks->{$pkg}) eq 'CODE') {
        $_ = $app_checks->{$pkg}();
    } else {
        $_ = `$app_checks->{$pkg}`;
    }
    if(! $_) {
        return (-1, 'not installed or error');
    }
    my ($ver) = m,(\d+\.\d+(?:\.\d+)?),;
    $ver ||= 0;
    return ($ver, '');
}

sub mk_uboot_kernel
{
    my ($vmlinuz, $pcf) = @_;
    return 1 unless $pcf->{DEPLOYMENT_U_BOOT_KERNEL};
    my $outpath = $pcf->{DEPLOYMENT_U_BOOT_KERNEL_PATH} || "vmlinux.gz.uboot";

    print "making vmlinux.gz.uboot\n";
    my $x = $verbose ? '-x' : '';
    system_nb(<<TXT) == 0 or return;
set -e
if [ -n "$x" ]; then set $x ; fi

rm -f vmlinux.gz.uboot

mkimage -n 'Linux for $pcf->{PLATFORM}' \\
        -A $pcf->{RPMTARCH} -O linux -T kernel -C gzip \\
        -a $pcf->{SYSCFG_RUNKERNELADDR} -e $pcf->{SYSCFG_RUNKERNELADDR} \\
        -d $vmlinuz $outpath
TXT
    return 1;
}

sub mk_fs_image
{
    my($rootfs, $pcf) = @_;
    return 1 if $pcf->{DEPLOYMENT_NFS};

    die("$rootfs directory missing\n") unless -d $rootfs;

    my ($stage, $dev_tab) = ("$rootfs.tmp", '');

    # figure out which device table to use
    if($pcf->{PKG_DEV}) { 
        # static device nodes
        if($pcf->{DEPLOYMENT_ROMFS}) {
            $dev_tab = 'bin/device_genromfs.txt';
        } else {
            $dev_tab = 'bin/device_table.txt';
        }
    } else {
        # dynamic device nodes
        if($pcf->{DEPLOYMENT_ROMFS}) {
            $dev_tab = 'bin/device_genromfs_min.txt';
        } else {
            $dev_tab = 'bin/device_table_min.txt';
        }

    }
    warn("device table: $dev_tab missing"), return unless -e $dev_tab;
    warn("using device table: $dev_tab\n") if $verbose;

    my $tdir = readpipe "echo -n $pcf->{DEPLOYMENT_ROOTFS_DIR}" || ".";
    warn("target dir '$tdir' does not exist\n"), return unless -d $tdir;

    # this turns of Use of uninitialized value in concatenation warnings
    local $^W = 0;

    print "making filesystem image file\nstaging directory is $stage\n";

    my $x = $verbose ? '-x' : '';
    my $v = $verbose ? '-v' : '';
    my $cmd;
    my $cur_date = gm_yyyymmdd();
    my $elf_datestamp = $pcf->{DEPLOYMENT_ELF_DATESTAMP} ? "-$cur_date" : "";

    system_nb(<<TXT);
set -e
if [ -n "$x" ]; then set $x ; fi
rm -rf $stage
if [ "$pcf->{DEPLOYMENT_RAMDISK}" = "y" ]
then
    rm -f $tdir/rootfs.ext2 $tdir/rootfs.ext2.gz $tdir/rootfs.ext2.gz.uboot
    rm -f $tdir/rootfs_image
fi
if [ "$pcf->{DEPLOYMENT_JFFS2}" = "y" ]
then
    rm -f $tdir/rootfs.jffs2
fi
if [ "$pcf->{DEPLOYMENT_YAFFS2}" = "y" ]
then
    rm -f $tdir/rootfs.yaffs2
fi
if [ "$pcf->{DEPLOYMENT_CRAMFS}" = "y" ]
then
    rm -f $tdir/cramfs.*
fi
if [ "$pcf->{DEPLOYMENT_ROMFS}" = "y" ]
then
    rm -f $tdir/image.bin $tdir/tmp/romfs.img $tdir/image.bin.gz
fi
if [ "$pcf->{DEPLOYMENT_INITRAMFS}" = "y" ]
then
    rm -f $tdir/initramfs.cpio.gz $tdir/initramfs.cpio.gz.uboot
fi
    mkdir -p $stage
TXT

    # copy the rootfs directory tree to the staging area
    print "Copying from $rootfs to staging area $stage\n" if $v;
    # This command only works if $stage is an absolute path.  It
    # should be, but check just to make sure.
    $stage =~ m,^/, or die "Stage directory '$stage' must use absolute path";
    system_nb(<<TXT) == 0 or return;
cd $rootfs
find . -perm -444 ! -type b ! -type c -print0 | cpio -p0d --quiet $stage
TXT

    if($pcf->{DEPLOYMENT_HL2SL}) {
        print("converting hard links to symlinks\n");
        find( { wanted => 
            sub { 
                my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev) = lstat;
                return unless(!S_ISDIR($mode) && $nlink > 1);
                push @{$hl->{$ino}}, $_;
              }, no_chdir => 1 }, $stage);

        foreach my $ino (keys %{$hl}) {
            my $src = @{$hl->{$ino}}[0];
            $src =~ s,$stage,,;
            for(my $i = 1 ; $i < @{$hl->{$ino}} ; $i++) {
                my $tgt = @{$hl->{$ino}}[$i];
                unlink($tgt) or warn("cannot remove: $tgt: $!");
                warn("symlink $src, $tgt\n") if $verbose;
                symlink($src, $tgt) or warn("symlink src, $tgt: $!")
            }
        }
    }

    # cleanup the staging area
    system_nb(<<TXT) == 0 or return;
set -e
if [ -n "$x" ]; then set $x ; fi
if [ "$pcf->{DEPLOYMENT_RM_BOOT}" = "y" ]
then
    echo "removing the boot directory and files"
    rm -rf $stage/boot
fi
if [ "$pcf->{DEPLOYMENT_RM_DOCS}" = "y" ]
then
    echo "removing man files and directories"
    rm -rf $stage/usr/share/man
    ####rm -rf $stage/usr/man
    echo "removing info files"
    rm -rf $stage/usr/info
fi
if [ "$pcf->{DEPLOYMENT_RM_USR_SRC}" = "y" ]
then
    echo "removing /usr/src directory"
    rm -rf $stage/usr/src
fi
if [ "$pcf->{DEPLOYMENT_RM_USR_INCLUDE}" = "y" ]
then
    echo "removing /usr/include directory"
    rm -rf $stage/usr/include
fi
if [ "$pcf->{DEPLOYMENT_RM_LOCALES}" = "y" ]
then
    echo "removing /usr/share/locale directory"
    rm -rf $stage/usr/share/locale
fi
if [ "$pcf->{DEPLOYMENT_RM_USER_DIRS}" != "" ]
then
    for i in $pcf->{DEPLOYMENT_RM_USER_DIRS}
    do
        if [ -d $stage/\$i ]
        then
            echo "removing \$i directory"
            rm -rf $stage/\$i
        fi
    done
fi
if [ "$pcf->{DEPLOYMENT_RM_USER_FILES}" != "" ]
then
    set -f
    for i in $pcf->{DEPLOYMENT_RM_USER_FILES}
    do
        set +f
        for j in $stage/\$i
        do
            if [ -e \$j ]
            then
                echo "removing file `echo \$j|perl -pe 's{^$stage/}{}'`"
                rm -f \$j || echo Error removing \$j
            fi
        done
    done
fi
if [ "$pcf->{DEPLOYMENT_RM_STATIC_LIBS}" = "y" ]
then
    echo "removing static libraries"
    find $stage -name \\*.a -exec rm -f {} \\;
fi
RPMDB=`echo $pcf->{DEPLOYMENT_RM_RPMDB}`
if [ "\$RPMDB" != "" -a  -d $stage/\$RPMDB ]
then
    echo "removing target rpm database" 
    rm -rf $stage/\$RPMDB
    rm -rf $stage/*/\$RPMDB
fi
if [ "$pcf->{DEPLOYMENT_STRIP}" = "y" ]
then
    echo "stripping binaries and libraries"
    if [ "$pcf->{DEPLOYMENT_STRIP_MORE}" = "y" ]
    then
       stripall -s -a $v $stage
    else
       stripall -s $v $stage
    fi
fi
TXT

    # calculate the size of the rootfs (based on calcs in buildroot)
    my $fs_count = 0;
    find( sub { $fs_count++ }, $stage);
    my ($fs_size) =  split(/\s+/, `LANG=C du -slk $stage`);
    $fs_size += $fs_size >= 20000 ? 16384 : 2400;
    $fs_size += $pcf->{DEPLOYMENT_PADDING_KB} if $pcf->{DEPLOYMENT_PADDING_KB};
    print <<TXT;

Filesystem stats, including padding:

    Total size            = ${fs_size}k
    Total number of files = $fs_count

TXT
    my $fs_size_p10 = int($fs_size * 1.1);

    if($fs_size > 4096) {
        print <<TXT if $pcf->{DEPLOYMENT_RAMDISK};
Your ramdisk exceeds the old default size of 4096k, you may need to
set the command line argument for ramdisk_size in your bootloader
allowing 10% free this gives ${fs_size_p10}k .  For instance, for u-boot:


setenv bootargs root=/dev/ram rw ramdisk_size=$fs_size_p10

TXT
    }
    # genext2fs seems to use 1k block size
    my $blocks = $fs_size;
    my $inodes = $fs_count + 400;

    # try to sanely guess the endian of the target
    my $endian = '-l';
    $pcf->{ENDIAN} ||= "b";
    $endian = "-b" if $pcf->{ENDIAN} =~ /b/i;
    warn "ENDIAN=$pcf->{ENDIAN}, endian=$endian\n" if $verbose;

    # calculate the size to pad out the jffs2 fs.  If padding was asked
    # for then use the actual FS size, otherwise leave it blank.
    my $pad_opt  = '-p';
    $pad_opt = '--pad=' . ($pcf->{DEPLOYMENT_JFFS2_IMAGE_SIZE} * 1024)
                                        if $pcf->{DEPLOYMENT_JFFS2_IMAGE_SIZE};

    system_nb(<<TXT) == 0 or return;
if [ -n "$x" ]; then set $x ; fi
set -e
if [ "$pcf->{DEPLOYMENT_RAMDISK}" = "y" ]
then
    echo "creating an ext2 compressed filesystem image: rootfs.ext2.gz"
    genext2fs -U -b $blocks -i $inodes -D $dev_tab -d $stage $tdir/rootfs.ext2
    gzip $tdir/rootfs.ext2
    if [ "$pcf->{DEPLOYMENT_RAMDISK_U_BOOT}" = "y" ]
    then
        echo "creating a uboot ramdisk image: rootfs.ext2.gz.uboot"
        mkimage -n 'uboot ext2 ramdisk rootfs' \\
            -A $pcf->{RPMTARCH} -O linux -T ramdisk -C gzip \\
            -d $tdir/rootfs.ext2.gz $tdir/rootfs.ext2.gz.uboot
    fi
    ln -sf $tdir/rootfs.ext2.gz.uboot $tdir/rootfs_image
else
    rm -f $tdir/rootfs.ext2.gz.uboot
fi
if [ "$pcf->{DEPLOYMENT_JFFS2}" = "y" ]
then
    mkfs.jffs2 -n $pad_opt -D $dev_tab -U $endian -e $pcf->{DEPLOYMENT_ERASE_BLOCK_SIZE} -d $stage -o $tdir/rootfs.jffs2
    ln -sf $tdir/rootfs.jffs2 $tdir/rootfs_image
fi
if [ "$pcf->{DEPLOYMENT_YAFFS2}" = "y" ]
then
    mkfs.yaffs2 -r -p $stage/etc/passwd -N -D $dev_tab $endian $stage $tdir/rootfs.yaffs2
    ln -sf $tdir/rootfs.yaffs2 $tdir/rootfs_image
fi
if [ "$pcf->{DEPLOYMENT_CRAMFS}" = "y" ]
then
    mkfs.cramfs -q -D $dev_tab $endian $stage $tdir/rootfs.cramfs
    ln -sf $tdir/rootfs.cramfs $tdir/rootfs_image
fi
if [ "$pcf->{DEPLOYMENT_ROMFS}" = "y" ]
then
    echo "creating romfs filesystem"
    for device in \$(tr -cs '[:graph:]' '[\n*]' < $dev_tab); \\
        do touch $stage/dev/\@\$device; done
    genromfs -V "ROMdisk" -d $stage -f $tdir/tmp/romfs.img
    ln -sf $tdir/romfs.img $tdir/rootfs_image
    if [ "$pcf->{KERNEL_NONE}" != "y" ]
    then
        cat $rootfs/boot/bootable_kernel $tdir/tmp/romfs.img > $tdir/image.bin
        if [ "$pcf->{DEPLOYMENT_ZIP}" = "y" ]
        then
            echo "compressing romfs/kernel filesystem"
            gzip -c -8 $tdir/image.bin > $tdir/image.bin.gz
            if [ "$pcf->{DEPLOYMENT_UIMAGE}" = "y" ]
            then
                echo "creating uImage"
                mkimage -A $pcf->{U_BOOT_IMAGE_TYPE} -O linux -T kernel -C gzip \\
                -a $pcf->{SYSCFG_RUNKERNELADDR} -e $pcf->{SYSCFG_RUNKERNELADDR} \\
                -n "Linux Kernel Image" -d $tdir/image.bin.gz $tdir/uImage
            fi
        fi
        if [ "$pcf->{DEPLOYMENT_SREC}" = "y" ]
        then
            echo "creating srec files"
            objcopy -O srec -I binary $tdir/image.bin $tdir/image.bin.srec
            if [ "$pcf->{DEPLOYMENT_ZIP}" = "y" ]
            then
                objcopy -O srec -I binary $tdir/image.bin.gz $tdir/image.bin.gz.srec
                rm -f $tdir/image.bin.gz
                ln -sf $tdir/image.bin.gz.srec $tdir/rootfs_image
            fi
        fi
    fi
fi
if [ "$pcf->{DEPLOYMENT_INITRAMFS}" = "y" ]
then
    echo "creating an initamfs compressed filesystem image: initramfs.cpio.gz"
    geninitramfs -U -D $dev_tab -d $stage | gen_init_cpio - | gzip -9 > $tdir/initramfs.cpio.gz
    # Note: not supported in dash (sigh)
    if [ -n "\$PIPESTATUS" -a \$PIPESTATUS -ne 0 ]
    then
        exit 1
    fi
    if [ "$pcf->{DEPLOYMENT_RAMDISK_U_BOOT}" = "y" ]
    then
        echo "creating a uboot initramfs image: initramfs.cpio.gz.uboot"
        mkimage -n 'uboot initramfs rootfs' \\
            -A $pcf->{RPMTARCH} -O linux -T ramdisk -C gzip \\
            -d $tdir/initramfs.cpio.gz $tdir/initramfs.cpio.gz.uboot
        ln -sf $tdir/initramfs.cpio.gz.uboot $tdir/rootfs_image
    fi
fi
if [ "$pcf->{DEPLOYMENT_ELF}" = "y" ]
then
    elf_image="linux-demo-$pcf->{PLATFORM_ELF}$elf_datestamp.elf"
    if [ "$pcf->{DEPLOY_RAMDISK_AND_ELF}" = "y" ]
    then
        echo "creating elf file that contains u-boot, kernel, ramdisk"
        make -C \$PLATFORM_PATH/elf-image elf-with-rootfs UBOOT=$cf->{top}/rootfs/boot/u-boot.bin KERNEL=$cf->{top}/rootfs/boot/uImage ROOTFS=$cf->{top}/rootfs.ext2.gz.uboot IMAGE=$cf->{top}/\$elf_image
    else
        echo "creating elf file that contains u-boot, kernel, rootfs assumed elsewhere"
        make -C \$PLATFORM_PATH/elf-image elf-without-rootfs UBOOT=$cf->{top}/rootfs/boot/u-boot.bin KERNEL=$cf->{top}/rootfs/boot/uImage IMAGE=$cf->{top}/\$elf_image
    fi
    ln -sf \$elf_image image.elf
fi

if [ "$pcf->{DEPLOYMENT_ROOTFS_KEEPSTAGE}" = "y" ]
then
    echo "Saving temporary staging directory: $stage"
else
    rm -rf $stage
fi
TXT
    return 1;
}

sub cmd_w_to
{
    my($timeout, @cmd) = @_;
    my $cmd_op;

    local $SIG{ALRM} = sub { die "timeout" };
    eval {
        alarm($timeout);
        $cmd_op = `@cmd`;
        alarm(0);
    };
    return $cmd_op unless $@;
    warn("caught timeout: @cmd\n"), return if $@ =~ /timeout/;
    warn("$@: @cmd\n"), return;
}

# Normally system will block SIGINT and SIGQUIT
# We don't want to do this, or we can't properly CNTRL-C ltib
sub system_nb
{
    return 0 if $cf->{dry};
    my (@cmd) = @_;
    if(my $pid = fork) {
        waitpid($pid, 0);
        return $?;
    } else {
        die "cannot fork: $!" unless defined $pid;
        exec(@cmd) or die "exec: @cmd: $!";
    }
}

sub check_scm_id_is_remote
{
    return 1 unless -d "$cf->{top}/.git";

    my ($id) = @_;
    return if `git cherry origin/master $id` =~ m,^\+,m;
    return 1;
}

sub get_scm_branch
{
    my $branch;

    if(-d "$cf->{top}/.git") {
        ($branch) = `git branch` =~ m,\* (.+),;
        return $branch;
    }

    # For CVS, the Tag file's first letter mean:
    # T : branch, N : nonbranch, D : date
    my $tagfile = 'CVS/Tag';
    return unless -f $tagfile;
    open(TAG, $tagfile) or die("Can't open $tagfile : $!");
    chomp($branch = <TAG>);
    close TAG;
    $branch = substr($branch,1);
    return $branch;
}

sub get_scm_tags
{
    return $scmtags if %$scmtags;

    my $tags;
    if(-d "$cf->{top}/.git") {
        open(GIT, "git tag -l |") or die;
        while(<GIT>) {
            chomp;
            $scmtags->{$_} = 1;
        }
        close GIT;
        return $scmtags;
    }

    if(-d "$cf->{top}/CVS") {
        open(CVSLOG, "cvs log 2>/dev/null |") or die;
        while(<CVSLOG>) {
            if( m,^\s+([^\s]+):\s+\d,) {
                $scmtags->{$1} = 1;
            }
        }
        close CVSLOG;
        return $scmtags;
    }

    return;
}

sub get_scm_tag
{
    my $tag;
    if(-d "$cf->{top}/.git") {
        chomp($tag = `bin/setlocalversion`);
        return $tag;
    }
    if(-f "$cf->{top}/CVS/Entries") {
        ($tag) = `cat CVS/Entries`  =~ m,/ltib/([^/]+),;
        return $tag;
    }
    return;
}

sub src_tree_is_clean
{
    if(-d "$cf->{top}/.git") {
        return get_scm_tag() =~ m,-dirty, ? 0 : 1;
    }

    if(-d "$cf->{top}/CVS") {
        return `cvs -nq up 2>&1` =~ m,^(?:C|M|U|A|R),m ? 0 : 1;
    }

}

sub tag_repository
{
    my ($tag) = @_;
    if(-d "$cf->{top}/.git") {
        die("TODO: how do you tag a git repository");
    }

    if(-d "$cf->{top}/CVS") {
        system_nb("cvs tag -c $tag .") == 0 or return;
    }

    return 1;
}

sub export_repository
{
    my ($tag, $dir) = @_;
    die("export dir: $dir exists") if -d $dir;

    if(-d "$cf->{top}/.git") {
        # don't assume we have -o pipefail or $PIPESTATUS
        my $cmd = "git archive --prefix=$dir/ $tag 2>git_errors| tar xf -";
        system_nb($cmd);
        my $git_errors = `cat git_errors` if -s 'git_errors';
        unlink('git_errors');
        warn("$cmd\n    $git_errors"), return if $git_errors;
    }

    if(-d "$cf->{top}/CVS") {
        system_nb("cvs export -kv -d $dir -r $tag ltib") == 0 or return;
    }

    return 1;


}


sub caller_stack
{
    my $i = shift || 0;
    my ($pack, $savpack, $savline, $line, $subname);
    my $ci = "";
    while( ($pack, undef, $line, $subname) = caller($i)) {
        $ci .= " " x (($i -1)*1) . "$subname:$savline\n" if $savline;
        $savline = $line;
        $savpack = $pack;
        $i++;
    }
    $ci .= " " x (($i -1)*1) . "$savpack:$savline\n";
    return $ci;
}

sub write_file
{
    my ($path, $buf) = @_;
    unlink($path);
    open(F, ">$path") or die("open >$path : $!");
    chmod(0664, $path);
    print F $buf;
    close F;
    return 1;
}

sub try_lock_file
{
    my ($lf, $lockinfo) = @_;
    sysopen($lf, $lf, O_RDWR|O_CREAT) or die("can't open $lf: $!\n");
    chmod(0666, $lf);

    if( flock($lf, LOCK_EX|LOCK_NB) ) {
        #flock($lf, LOCK_EX) or die("can't lock $lf: $!\n");
        seek($lf, 0, 0)     or die("can't seek to start of $lf: $!\n");
        truncate($lf, 0)    or die("can't truncate $lf $!\n");
        my $ofh = select($lf); $| = 1; select($ofh);
        print($lf $lockinfo);
        return(1);
    }
    return;
}

sub release_lock_file
{
    my($lf) = @_;
    close($lf);
    unlink($lf);
}


1;

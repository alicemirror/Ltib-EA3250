######################################################################
#
# Copyright © Freescale Semiconductor, Inc. 2004-2008. All rights reserved.
#
# Stuart Hughes, stuarth@freescale.com, 29th April 2008
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
# Module to list packages in various formats
#
#
######################################################################
package main;
use File::Find;

sub listpkgs
{
   my ($mode) = shift || 'text';
   warn("listpkgs: invalid mode/format: $mode\n"), return unless $mode =~ m,^(?:text|twiki|eula|csv|build)$,;

   my ($tok, $en, $sn, $sep);
   $sep = "\t";
   $^L = '';
   if ($mode eq 'eula' || $mode eq 'csv') {
       # Set large FORMAT_LINES_PER_PAGE so there is only one page
       $= = 10000;
   }
   # Set FORMAT_NAME
   $~ = $mode;
   $^ = $mode . "_top";

format text_top =
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<< @|||||| @<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'-----------------------','----------------','-------','-------','-----------------------------------------'
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<< @|||||| @<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'Package', 'Spec file', 'Enabled','License','Summary'
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<< @|||||| @<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'-----------------------','----------------','-------','-------','-----------------------------------------'
.
format text =
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<< @|||||| @<<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$tok->{name}.'-'.$tok->{version}.'-'.$tok->{release}, $sn, $en, $tok->{license}, $tok->{summary}
.
format twiki_top =
@<@<<<<<<<<<<<<<<<<<<<<<<<<<<@<@<<<<<<<<<<<<<<<<<<<<<<@<@|||||@<@<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<@<@*@<
'|','*Package*','|','*Spec Name*','|','*En*','|','*Summary*','|','*License*','|'
.
format twiki =
@<@<<<<<<<<<<<<<<<<<<<<<<<<<<@<@<<<<<<<<<<<<<<<<<<<<<<@<@|||||@<@<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<@<@*@<
'|',$tok->{name}.'-'.$tok->{version}.'-'.$tok->{release},'|',$sn,'|',$en,'|',$tok->{summary},'|',$tok->{license},'|'
.
format eula_top =
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<
'Package', 'License'
@<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<<<
'-----------------------','-------'
.
format eula =
@<<<<<<<<<<<<<<<<<<<<<<< @*
"$tok->{name}-$tok->{version}-$tok->{release}", $tok->{license}
.

format csv_top = 
@<<<<<<<<<<<<<<<<<<<<<<<@*@||||||@*@*@*@*
'Package', $sep, 'Enabled', $sep, 'License', $sep, 'Description'
.
format csv =
@<<<<<<<<<<<<<<<<<<<<<<<@*@||||||@*@*@*@*
"$tok->{name}-$tok->{version}-$tok->{release}", $sep, $en, $sep, $tok->{license}, $sep, $tok->{summary}
.

format build_top = 
@<<<<<<<<<<<<<<<<<<<<<<<@*@*@*@*
'Package', $sep, 'License', $sep, 'Description'
.
format build =
@<<<<<<<<<<<<<<<<<<<<<<<@*@*@*@*
"$tok->{name}-$tok->{version}-$tok->{release}", $sep, $tok->{license}, $sep, $tok->{summary}
.
  
   my @pkg_list = get_key_list();
   @pkg_list = sort { $$a->{sn} cmp $$b->{sn} } @pkg_list if $mode ne 'build';
   foreach my $key ( @pkg_list ) {
       next if !$$key->{en} && $mode eq 'build';
       next if $cf->{enabled} && $$key->{en} == 0;
       $sn = $$key->{sn};
       $en = $$key->{en} ? 'y' : 'n';
       my $spec = get_spec($sn) or warn("skipping $sn\n"), next;
       $tok = parse_spec($spec) or die();
       write;
   }
   return 1;
}

sub get_key_list
{
    die("Please specify the preconfig to list, or configure your ltib\n")
                            if ! -f "$cf->{top}/.config" && ! $cf->{upreconfig};
    $cf->{upreconfig} =~ s,/\s*$,,   if $cf->{upreconfig};
    $cf->{batch} = 1;
    check_dirs();
    $cf->{plat_dir} = get_plat_dir();
    ltib_config();
    pkg_cache_init();
    $pcf = parse_dotconfig($cf->{preconfig});

    return mk_buildlist();
}


1;

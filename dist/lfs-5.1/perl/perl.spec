%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The Perl programming language
Name            : perl
Version         : 5.8.8
Release         : 2
License         : Artistic or GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Development/Languages
Source          : perl-5.8.8.tar.gz
Source1         : perl-5.8.8-Glob_pm.simple
Source2         : perl-5.8.8-config_sh_macg4
Patch1          : perl-5.8.8-gcc-4.2.patch
Patch2          : perl-5.8.8-dash-shell.patch
Patch3          : perl-5.8.8-asm-page-header.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
# perl auto module dependency is pretty broken in rpm, so we have
# to turn off all dependency checks
Autoreqprov     : no


%Description
%{summary}

%Prep
%setup
%patch1 -p1 
%patch2 -p1
%patch3 -p1 

%Build
#
# build a version for the machine we are building on, before we
# build for the target
#
ORIG_PATH=$PATH
export PATH=$UNSPOOF_PATH
if [ ! -f build-perl ]
then
    rm -rf native-build
    mkdir native-build
    cd native-build

    # seed some options for the build machine perl build
    # that can be guessed incorrectly
    cat <<EOF > config.over
static_ext=' '
perllibs='-lnsl -ldl -lm -lc -lcrypt -lutil'
EOF

    ENDIAN=${ENDIAN:-big}
    case $ENDIAN in
        big) echo byteorder='4321' >> config.over;;
        *)   ;;
    esac
 
    # configure: config.over will override the guesses
    sh ../Configure -O -Dmksymlinks \
    -Dprefix=%{_prefix} \
    -des -Accflags=-DNO_LOCALE -Dcc=gcc 
    make miniperl perl
    cd -
    for i in miniperl perl
    do
       cp native-build/$i build-$i
    done
fi

#
# build Perl to run on the target
#
export PATH=$ORIG_PATH

# Use a generic ppc perl config.sh and fixup as needed
cp -f %{SOURCE2} config.sh
./build-perl -pi.orig -e '
                ### maybe we need to do this ? s,^byteorder=.*,,;
                s,ppc-linux,$ENV{LINTARCH}-linux,g;
                s,^xlibpth=.*,xlibpth="/usr/lib/$ENV{LINTARCH} /lib/$ENV{LINTARCH}",;
                s,^src=.*,src=$ENV{PWD},;
                                                  ' config.sh

# fixup the other configuration build files
./build-perl -pi.orig -e '
                s,\./miniperl,./build-miniperl,g;
                s,\./perl,./build-perl,g;
                                                  ' Makefile.SH
./build-perl -pi.orig -e '
                s,/miniperl,/build-miniperl,g;
                                                  ' x2p/Makefile.SH
./build-perl -pi.orig -e '
                s,/miniperl,/build-miniperl,g;
                                                  ' ext/util/make_ext
./build-perl -pi.orig -e '
                s,/miniperl,/build-miniperl,g;
                                                  ' utils/Makefile
./build-perl -pi.orig -e '
                s,die "You must run as root,warn "You must run as root,;
                                                  ' installperl

if [ ! -f ext/File/Glob/Glob.pm.orig ]
then
    mv ext/File/Glob/Glob.pm ext/File/Glob/Glob.pm.orig
    cp -f %{SOURCE1} ext/File/Glob/Glob.pm.simple
    cp ext/File/Glob/Glob.pm.simple ext/File/Glob/Glob.pm
fi

# there is something wrong with the makedepends, this is harmless and
# fixes the problem.  It only occurs on re-started builds
touch wince.h nwutil.h

./Configure -S
make depend
make


%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
cp -af ext/File/Glob/Glob.pm.orig $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/perl5/%{version}/${LINTARCH}-linux/File/Glob.pm


%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



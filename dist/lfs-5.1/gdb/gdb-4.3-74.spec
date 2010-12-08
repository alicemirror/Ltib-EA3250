%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define cs_version 4.3-74

Summary         : Gdb - GNU Source level debugger for C, C++
Name            : gdb
Version         : 6.6
Release         : 3
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes/Steve Papacharalambous
Group           : Development/Debuggers
Source          : %{name}-%{version}.tar.gz
Patch0          : gdb-6.0-tcsetpgrp.patch
Patch1          : %{name}-%{cs_version}-from-fsf-6_6.diff.bz2
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

Notes:

This gdb package is built using gdb-6.6 plus the gdb patch from the
CodeSourcery %{cs_version} release: gdb-%{cs_version}-from-fsf-6_6.diff

The gdb tarball can be obtained from any of the GNU ftp sites or their mirrors.
The CodeSourcery patch can be obtained by downloading the source rpm:
freescale-powerpc-linux-gnu-%{cs_version}.src.rpm from:
http://www.codesourcery.com/gnu_toolchains/power/download.html and then
extracting the gdb patch from this source rpm.

requires: libtermcap and ncurses


%Prep
%setup
%patch0 -p1
%patch1 -p1

# Temporary hack.  Stevep
# This is to prevent the following error occuring on some build systems:
# [snip]
# Doing pdf in readline
# make[3]: Entering directory `/home/stevep/work/ltib/rpm/BUILD/gdb-6.6/readline'
# ( cd doc && make -w pdf )
# make[4]: Entering directory `/home/stevep/work/ltib/rpm/BUILD/gdb-6.6/readline/doc'
# TEXINPUTS=.:../.././readline/doc:$TEXINPUTS ../.././readline/doc/texi2dvi ../.././readline/doc/rlman.texi
# This is TeX, Version 3.14159 (Web2C 7.3.1)
# (/home/stevep/work/ltib/rpm/BUILD/gdb-6.6/readline/doc/rlman.texi
# (/usr/share/texmf/tex/texinfo/texinfo.tex
# Loading texinfo [version 1999-09-25.10]: Basics, pdf, fonts, page headings,
# tables, conditionals, indexing, sectioning, toc, environments, defuns, macros,
# cross references, (/usr/share/texmf/tex/plain/dvips/epsf.tex) localization,
# and turning on texinfo input format.) (rlman.aux) (version.texi)
# ! Undefined control sequence.
# l.11 @copying
#              
# ? 
# [/snip]
perl -pi.orig -e 's,^\@copying,\@comment \@copying,;
                  s,^\@end\s+copying,\@comment \@end copying,;
                  s,^\@insertcopying,\@comment \@insertcopying,;' readline/doc/rlman.texi

perl -pi.orig -e 's,^\@copying,\@comment \@copying,;
                  s,^\@end\s+copying,\@comment \@end copying,;
                  s,^\@insertcopying,\@comment \@insertcopying,;' readline/doc/history.texi

perl -pi.orig -e 's,^\@copying,\@comment \@copying,;
                  s,^\@end\s+copying,\@comment \@end copying,;
                  s,^\@insertcopying,\@comment \@insertcopying,;' readline/doc/rluserman.texi


%Build
ORIG_PATH=$PATH
# This is the optimised host type.  Needed to prevent infering a native build
OPT_CFGHOST=`echo ${TOOLCHAIN_PREFIX} | perl -n -e 's,-$,,;print'`


# Ensure that build is never the same as host.
GDB_BUILD=`echo %{_build} | sed s/-/-build_/`


# Test for the presence of the exexutable /usr/bin/xmlwf to determine whether
# the version of expat on the host system is recent enough to provide support
# for cross-gdb xml.
if [ -x /usr/bin/xmlwf ]
then
    HOST_EXPAT_TOO_OLD="no"
else
    HOST_EXPAT_TOO_OLD="yes"
fi


# do something (the least costly)
if [ -z "$PKG_GDB_CROSS_WANT_ED$PKG_GDB_SERVER_WANT_ED$PKG_GDB_NATIVE_WANT_ED" ]
then
    PKG_GDB_SERVER_WANT_ED=y
fi

if [ -z "$PKG_GDB_XML_WANT_ED" ]
then
    expat_opt='ac_cv_libexpat=no'
else
    expat_opt='ac_cv_libexpat=yes'
fi


# cross gdb to run on the build machine
if [ -n "$PKG_GDB_CROSS_WANT_ED" ]
then
    expat_opt_orig=${expat_opt}
    if [ ${HOST_EXPAT_TOO_OLD} = "yes" ]
    then
        expat_opt='ac_cv_libexpat=no'
        echo "The version of expat on the build host is too old to build"
        echo " cross gdb with xml support, so xml support for cross gdb"
        echo " has been disabled."
        echo "The version of expat on the build system must be 1.95.5 or"
        echo "greater for cross gdb xml support."
    fi

    BD=cross-gdb
    rm -rf $BD
    mkdir -p $BD
    cd $BD
    export PATH=$UNSPOOF_PATH
    export ac_cv_header_stdc=yes bash_cv_have_mbstate_t=yes \
           ac_cv_header_nlist_h=no ${expat_opt}
    ../configure --prefix=%{_prefix} --target=$CFGHOST --mandir=%{_mandir} --without-libexpat-prefix --disable-werror
    make
    cp gdb/gdb $TOP/bin/gdb
    cd -
    expat_opt=${expat_opt_orig}
fi

# from now build stuff to go into the rpm package
export PATH=$ORIG_PATH

# gdbserver to run on the target
if [ -n "$PKG_GDB_SERVER_WANT_ED" ]
then
    cd gdb/gdbserver
    export ${expat_opt}
    ./configure --prefix=%{_prefix} --host=$CFGHOST --mandir=%{_mandir} --without-libexpat-prefix --disable-werror
    make
    cd -
fi

# full gdb to run on the target
if [ -n "$PKG_GDB_NATIVE_WANT_ED" ]
then
    export CPP="$BUILDCPP"
    export CC_FOR_BUILD="$BUILDCC"
    export ac_cv_header_stdc=yes bash_cv_have_mbstate_t=yes \
           ac_cv_header_nlist_h=no ${expat_opt}
    CC=gcc AR=ar \
    ./configure --prefix=%{_prefix} --host=$OPT_CFGHOST --build=%{_build} --mandir=%{_mandir}  --without-libexpat-prefix --disable-werror --disable-sim
    # don't build gdbserver
    perl -pi.orig -e 's,(x\$build_gdbserver),$1_no_thanks,' gdb/configure
    make
fi

%Install
if [ -z "$PKG_GDB_CROSS_WANT_ED$PKG_GDB_SERVER_WANT_ED$PKG_GDB_NATIVE_WANT_ED" ]
then
    PKG_GDB_SERVER_WANT_ED=y
fi

if [ ${PKG_GDB_BUILD_DOCS} = "n" ]
then
perl -pi.bak -e 'if(m,^do-info\:$, || m,^do-dvi\:$, || m,^do-pdf\:$, || m,^do-html\:$, || m,^do-install-info\:$, || m,^do-install-pdf\:$, || m,^do-install-html\:$,) { $do_edit = 1; next }; if(m,^\.PHONY\:\s+info-host$, || m,^\.PHONY\:\s+dvi-host$, || m,^\.PHONY\:\s+pdf-host$, || m,^\.PHONY\:\s+html-host$, || m,^\.PHONY\:\s+install-info-host$, || m,^\.PHONY\:\s+install-pdf-host$, || m,^\.PHONY\:\s+install-html-host$,) { $do_edit = 0 }; if($do_edit) { print "#" }' Makefile
cd cross-gdb
perl -pi.bak -e 'if(m,^do-info\:$, || m,^do-dvi\:$, || m,^do-pdf\:$, || m,^do-html\:$, || m,^do-install-info\:$, || m,^do-install-pdf\:$, || m,^do-install-html\:$,) { $do_edit = 1; next }; if(m,^\.PHONY\:\s+info-host$, || m,^\.PHONY\:\s+dvi-host$, || m,^\.PHONY\:\s+pdf-host$, || m,^\.PHONY\:\s+html-host$, || m,^\.PHONY\:\s+install-info-host$, || m,^\.PHONY\:\s+install-pdf-host$, || m,^\.PHONY\:\s+install-html-host$,) { $do_edit = 0 }; if($do_edit) { print "#" }' Makefile
cd -
fi

rm -rf $RPM_BUILD_ROOT
if [ -n "$PKG_GDB_SERVER_WANT_ED" ]
then
    cd gdb/gdbserver
    make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
    cd -
fi
if [ -n "$PKG_GDB_NATIVE_WANT_ED" ]
then
    make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}
    # remove standards.info which conflicts with autoconf
    rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/info/standards.info
fi
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/*.la

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*



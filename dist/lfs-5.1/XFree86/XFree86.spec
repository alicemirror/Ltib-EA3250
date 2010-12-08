%define pfx /opt/freescale/rootfs/%{_target_cpu}
%define BLD_DIR XFree86

Summary         : X Windows System
Name            : XFree86
Version         : 4.4.0
Release         : 1
License         : XFree86 1.1 (BSD like)
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : System Environment/Libraries
Source0         : XFree86-4.4.0-src-1.tgz
Source1         : XFree86-4.4.0-src-2.tgz
Source2         : XFree86-4.4.0-src-3.tgz
Source3         : XFree86-4.4.0-src-4.tgz
Source4         : XFree86-4.4.0-src-5.tgz
Source5         : XFree86-4.4.0-src-6.tgz
Source6         : XFree86-4.4.0-src-7.tgz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}


%Prep
cd ${RPM_BUILD_DIR}
rm -rf %{BLD_DIR}
mkdir %{BLD_DIR}
cd %{BLD_DIR}

for i in XFree86-4.4.0-src-1.tgz XFree86-4.4.0-src-2.tgz XFree86-4.4.0-src-3.tgz XFree86-4.4.0-src-4.tgz XFree86-4.4.0-src-5.tgz XFree86-4.4.0-src-6.tgz XFree86-4.4.0-src-7.tgz
do
	DC=`perl -e 'shift =~ /bz2/ ? print "--bzip" : print "-z"' $i`
	tar ${DC} -xvf $RPM_SOURCE_DIR/$i
done

cd xc
cat > config/cf/host.def << "EOF"

#define BourneShell      bash 
#define CppCmd           cpp
#define RawCppCmd        cpp -undef
#define ModuleCppCmd     cpp
#define GccWarningOptions  -pipe /* Speed up compiles */
#define ForceNormalLib   YES


#define BuildLBX                NO
#define BuildFonts              NO
#define BuildAppgroup           NO
#define BuildDBE                NO
#define BuildXCSecurity         NO
#define FontServerAccess        NO
#define BuildFontServer         NO
#define BuildSpecsDocs          NO
#define BuildEVI                NO
#define BuildPlugin             NO
#define BuildRECORD             NO
#define BuildPexExt             NO
#define BuildServer             NO
#define BuildXAudio             NO
#define BuildXAServer           NO
#define BuildXIE                NO
#define BuildXInputExt          NO
#define BuildXInputLib          NO
#define BuildXKB                NO
 

/* use external packages for these */
#define HasFreetype2             YES
#define HasFontconfig            YES
#define HasExpat                 YES
#define HasLibpng                YES
#define HasZlib                  YES
#define HasTk                    NO
#define HasPam                   NO
#define HasKrbIV                 NO
#define HasKrb5                  NO

#define ProjectRoot      %{_prefix}/X11R6
#define VarDirectory     %{_prefix}/var
#define SystemUsrLibDir  %{_prefix}/lib
#define SystemUsrIncDir  %{_prefix}/include
#define LogDirectory     %{_prefix}/var/log
#define AdmDir           %{_prefix}/adm
#define Freetype2Dir     %{_prefix}
#define ExpatDir         %{_prefix}
#define FontconfigDir    %{_prefix}
#define LibpngDir        %{_prefix}
#define TkLibDir         %{_prefix}/lib
#define TkIncDir         %{_prefix}/include
#define TclLibDir        %{_prefix}/lib
#define TclIncDir        %{_prefix}/include
#define EtcX11Directory  %{_prefix}/etc/X11
#define XAppLoadDir      %{_prefix}/etc/X11/app-defaults

EOF

%Build
cd $RPM_BUILD_DIR/%{BLD_DIR}/xc

# This will build all makefiles etc, but nothing else, I only want libraries
make World WORLDOPTS=""

%Install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/%{BLD_DIR}/xc
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make DESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} install 
for i in bin lib include
do
    mkdir -p $RPM_BUILD_ROOT/${pfx}/%{_prefix}/$i
done
ln -sf ../X11R6/bin         $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/X11
ln -sf ../X11R6/lib/X11     $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/X11
ln -sf ../X11R6/include/X11 $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/X11

# fix some links that come out with absolute paths
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/GL
ln -sf ../X11R6/include/GL  $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/GL
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libGL.so
rm -f $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libGL.so.1
ln -sf ../X11R6/lib/libGL.so $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libGL.so 
ln -sf ../X11R6/lib/libGL.so.1 $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libGL.so.1

%Post
echo "%{_prefix}/X11R6/lib" >> %{_prefix}/etc/ld.so.conf
%{_prefix}/sbin/ldconfig


%Clean
rm -rf $RPM_BUILD_ROOT



%Files
%defattr(-,root,root)
%{pfx}/*



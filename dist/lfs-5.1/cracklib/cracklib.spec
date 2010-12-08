%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : A password-checking library.
Name            : cracklib
Version         : 2.8
Release         : 9
License         : GPL
Vendor          : Freescale
Packager        : Olivia Yin
Group           : Applications/System
Source          : %{name}-%{version}.%{release}.tar.gz
Source1         : cracklib-words.gz
Patch0          : cracklib-2.8.9-heimdal-1.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -n %{name}-%{version}.%{release}
%patch0 -p1

%Build
if [ -n "$UCLIBC" ]
then
    config_opts='gt_cv_func_gnugettext1_libintl=no'
fi
eval $config_opts \
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} -C
make

%Install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr
for i in lib share/dict/words
do
    mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/$i
done
mkdir -p $RPM_BUILD_ROOT/%{pfx}/lib/cracklib

make install PREFIX=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} \
             DESTDIR=$RPM_BUILD_ROOT/%{pfx} \ &&
mv -v /usr/lib/libcrack.so.2* /lib &&
ln -v -sf ../../lib/libcrack.so.2.8.0 /usr/lib/libcrack.so

install -v -m 644 -D /opt/freescale/pkgs/cracklib-words.gz \
    $RPM_BUILD_ROOT/%{pfx}/usr/share/dict/cracklib-words.gz &&
gunzip -v $RPM_BUILD_ROOT/%{pfx}/usr/share/dict/cracklib-words.gz &&
ln -v -s cracklib-words $RPM_BUILD_ROOT/%{pfx}/usr/share/dict/words &&
echo $(hostname) >>$RPM_BUILD_ROOT/%{pfx}/usr/share/dict/cracklib-extra-words &&
install -v -m 755 -d $RPM_BUILD_ROOT/%{pfx}/lib/cracklib &&
#create-cracklib-dict $RPM_BUILD_ROOT/%{pfx}/usr/share/dict/cracklib-words \
#                     $RPM_BUILD_ROOT/%{pfx}/usr/share/dict/cracklib-extra-words

find $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib -name \*.la -exec rm -f {} \;


%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*

%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The BSD database library for C (version 1).
Name            : db1
Version         : 1.85
Release         : 8
License         : BSD
Vendor          : Freescale
Packager        : Redhat 7.3 / Stuart Hughes
Group           : System Environment/Libraries
Source          : http://www.sleepycat.com/update/%{version}/db.%{version}.tar.gz
Patch0          : db.%{version}.patch
Patch1          : db.%{version}.s390.patch
Patch2          : db.%{version}.nodebug.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup -q -n db.%{version}
%patch0 -p1 -b .patch
%patch1 -p1 -b .fPIC
%patch2 -p1 -b .nodebug

%Build
gzip -9 docs/*.ps
cd PORT/linux
make

%Install
rm -rf $RPM_BUILD_ROOT
for i in include/db1 lib bin
do
    mkdir -p ${RPM_BUILD_ROOT}%{pfx}/%{_prefix}/$i
done
sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

perl -pi -e 's/<db.h>/<db1\/db.h>/' PORT/include/ndbm.h

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install -m644 libdb.a               $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libdb1.a
install -m755 libdb.so.$sover       $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libdb1.so.$sover
ln -sf libdb1.so.$sover             $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libdb1.so
ln -sf libdb1.so.$sover             $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/lib/libdb.so.$sover
install -m644 ../include/ndbm.h     $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/db1/
install -m644 ../../include/db.h    $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/db1/
install -m644 ../../include/mpool.h $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/db1/
install -m755 db_dump185            $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/bin/db1_dump185

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


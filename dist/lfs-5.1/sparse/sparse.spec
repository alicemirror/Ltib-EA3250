%define pfx /opt/freescale/rootfs/%{_target_cpu}

Name		: sparse
Version		: 0.4
Release		: 1
Summary		: A semantic parser of source files
Group		: Development/Tools
License		: Open Software License
URL		: http://kernel.org/pub/software/devel/sparse/
Source0		: %{name}-%{version}.tar.gz
Patch0          : %{name}-%{version}-array-fix.patch
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%description
Sparse is a semantic parser of source files: it's neither a compiler
(although it could be used as a front-end for one) nor is it a
preprocessor (although it contains as a part of it a preprocessing
phase).

It is meant to be a small - and simple - library.  Scanty and meager,
and partly because of that easy to use.  It has one mission in life:
create a semantic parse tree for some arbitrary user for further
analysis.  It's not a tokenizer, nor is it some generic context-free
parser.  In fact, context (semantics) is what it's all about - figuring
out not just what the grouping of tokens are, but what the _types_ are
that the grouping implies.

Sparse is primarily used in the development and debugging of the Linux kernel.

%prep
%setup -q
%patch0 -p1

%build
make DESTDIR=$RPM_BUILD_ROOT PREFIX="%{pfx}/%{_prefix}" CFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT PREFIX="%{pfx}/%{_prefix}" install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{pfx}/%{_prefix}/bin/*
%{pfx}/%{_prefix}/share/man/man1/*

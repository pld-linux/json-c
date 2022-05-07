#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	A JSON implementation in C
Summary(pl.UTF-8):	Implementacja JSON w C
Name:		json-c
Version:	0.16
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://s3.amazonaws.com/json-c_releases/releases/index.html # with AJAX (requires JavaScript)
# XML data with links (relative to https://s3.amazonaws.com/json-c_releases/) in https://s3.amazonaws.com/json-c_releases (no "/" at the end!)
Source0:	https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
# Source0-md5:	8110782cb2a996da5517f1f27a4bed8e
URL:		https://github.com/json-c/json-c/wiki
BuildRequires:	cmake >= 2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%description -l pl.UTF-8
JSON-C implementuje model obiektów ze zliczaniem odwołań, pozwalający
łatwo konstruować obiekty JSON w C, wypisywać je w postaci łańcuchów w
formacie JSON i analizować łańcuchy w formacie JSON tworząc z powrotem
reprezentacje obiektów JSON w C.

%package devel
Summary:	Header files for the json-c library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for the json-c library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki json-c.

%package static
Summary:	Static json-c library
Summary(pl.UTF-8):	Statyczna biblioteka json-c
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static json-c library.

%description static -l pl.UTF-8
Statyczna biblioteka json-c.

%prep
%setup -q

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%pretrans devel
# transition from 0.11-2
[ ! -L %{_includedir}/json-c ] || rm -f %{_includedir}/json-c
# transition from <= 0.10 and 0.11-2
if [ -d %{_includedir}/json -a ! -d %{_includedir}/json-c ]; then
	mv -f %{_includedir}/json %{_includedir}/json-c
	ln -sf json-c %{_includedir}/json
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.html
%attr(755,root,root) %{_libdir}/libjson-c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjson-c.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjson-c.so
%{_includedir}/json-c
%{_pkgconfigdir}/json-c.pc
%{_libdir}/cmake/json-c

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjson-c.a
%endif

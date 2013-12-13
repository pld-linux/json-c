Summary:	A JSON implementation in C
Summary(pl.UTF-8):	Implementacja JSON w C
Name:		json-c
Version:	0.11
Release:	3
License:	MIT
Group:		Libraries
Source0:	https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
# Source0-md5:	aa02367d2f7a830bf1e3376f77881e98
URL:		https://github.com/json-c/json-c/wiki
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
%configure
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# link with libjson-c directly (stub libjson won't work with --no-copy-dt-needed-entries
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libjson-c.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libjson.so

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
%attr(755,root,root) %{_libdir}/libjson.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjson.so.0
%attr(755,root,root) %{_libdir}/libjson-c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjson-c.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjson.so
%attr(755,root,root) %{_libdir}/libjson-c.so
%{_includedir}/json
%{_includedir}/json-c
%{_pkgconfigdir}/json.pc
%{_pkgconfigdir}/json-c.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libjson.a
%{_libdir}/libjson-c.a

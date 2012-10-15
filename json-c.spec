Summary:	A JSON implementation in C
Summary(pl.UTF-8):	Implementacja JSON w C
Name:		json-c
Version:	0.9
Release:	2
License:	MIT
Group:		Development/Libraries
Source0:	http://oss.metaparadigm.com/json-c/%{name}-%{version}.tar.gz
# Source0-md5:	3a13d264528dcbaf3931b0cede24abae
URL:		http://oss.metaparadigm.com/json-c/
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
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.html
%attr(755,root,root) %{_libdir}/libjson.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjson.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjson.so
%{_libdir}/libjson.la
%{_includedir}/json
%{_pkgconfigdir}/json.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libjson.a

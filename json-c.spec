Summary:	A JSON implementation in C
Name:		json-c
Version:	0.9
Release:	1
License:	LGPL v2
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

%package devel
Summary:	Header files for the json-c library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for the json-c library.

%package static
Summary:	Static json-c library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static json-c library.

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
%doc README INSTALL AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libjson.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjson.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/json
%attr(755,root,root) %{_libdir}/libjson.so
%{_libdir}/libjson.la
%{_pkgconfigdir}/json.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libjson.a

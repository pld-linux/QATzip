#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Intel QuickAssist Technology (QAT) QATzip library
Summary(pl.UTF-8):	Biblioteka QATzip wykorzystująca Intel QuickAssist Technology (QAT)
Name:		QATzip
Version:	1.1.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/QATzip/releases
Source0:	https://github.com/intel/QATzip/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e0f94367204ffda5e596983719a4b295
Patch0:		%{name}-types.patch
Patch1:		%{name}-flags.patch
URL:		https://github.com/intel/QATzip
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2.4
BuildRequires:	lz4-devel
BuildRequires:	pkgconfig
BuildRequires:	qatlib-devel >= 22.07.0
BuildRequires:	zlib-devel >= 1.2.7
Requires:	zlib >= 1.2.7
# x86_64-specific hardware, allow userspace libs for all ABIs
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QATzip is a user space library which builds on top of the Intel(R)
QuickAssist Technology user space library, to provide extended
accelerated compression and decompression services by offloading the
actual compression and decompression request(s) to the Intel(R)
Chipset Series. QATzip produces data using the standard gzip format
(RFC1952) with extended headers. The data can be decompressed with a
compliant gzip implementation. QATzip is designed to take full
advantage of the performance provided by Intel(R) QuickAssist
Technology.

%description -l pl.UTF-8
QATzip to biblioteka przestrzeni użytkownika, oparta na bibliotece
Intel(R) QuickAssist Technology, zapewniająca usługi rozszerzonej,
akcelerowanej kompresji i dekompresji przez delegowanie właściwych
żądań kompresji i dekompresji do układów chipsetu firmy Intel. QATzip
produkuje dane przy użyciu standardowego formatu gzip (RFC1952) z
rozszerzonymi nagłówkami. Dane mogą być dekompresowane przy użyciu
zgodnej implementacji gzipa. QATzip został zaprojektowany tak, aby w
pełni wykorzystywać wydajność zapewnianą przez Intel(R) QuickAssist
Technology.

%package devel
Summary:	Header files for QATzip library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki QATzip
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lz4-devel
Requires:	qatlib-devel >= 22.07.0
Requires:	zlib-devel >= 1.2.7

%description devel
Header files for QATzip library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QATzip.

%package static
Summary:	Static QATzip library
Summary(pl.UTF-8):	Statyczna biblioteka QATzip
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static QATzip library.

%description static -l pl.UTF-8
Statyczna biblioteka QATzip.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libqatzip.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md SECURITY.md
%attr(755,root,root) %{_bindir}/qzip
%attr(755,root,root) %{_libdir}/libqatzip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqatzip.so.3
%{_mandir}/man1/qzip.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqatzip.so
%{_includedir}/qatzip.h
%{_pkgconfigdir}/qatzip.pc

%if %{without static}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqatzip.a
%endif

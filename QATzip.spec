Summary:	Intel QuickAssist Technology (QAT) QATzip library
Summary(pl.UTF-8):	Biblioteka QATzip wykorzystująca Intel QuickAssist Technology (QAT)
Name:		QATzip
Version:	1.0.7
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/QATzip/releases
Source0:	https://github.com/intel/QATzip/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d0c09f5f95c3468f5731b4a42b956b7e
Patch0:		%{name}-types.patch
URL:		https://github.com/intel/QATzip
BuildRequires:	qatlib-devel
BuildRequires:	zlib-devel
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

%description devel
Header files for QATzip library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QATzip.

%prep
%setup -q
%patch0 -p1

%build
# --build is just to omit -m$(getconf LONG_BIT)
./configure \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix=%{_prefix} \
	--sharedlib-dir=%{_libdir} \
	--staticlib-dir=%{_libdir} \
	--mandir=%{_mandir} \
	--build=set

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_mandir}/QATzip-man.pdf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/qzip
%attr(755,root,root) %{_libdir}/libqatzip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqatzip.so.1
%{_mandir}/man1/qzip.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqatzip.so
%{_includedir}/qatzip.h

#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	pickleshare
Summary:	A small 'shelve' like datastore with concurrency support
Summary(pl.UTF-8):	Mały, podobny do 'shelve', zarządca danych z obsługą współbieżności
Name:		python-%{module}
Version:	0.7.5
Release:	7
License:	MIT
Group:		Libraries/Python
#Source0Download: https://github.com/pickleshare/pickleshare/releases
Source0:	https://github.com/pickleshare/pickleshare/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	79387de9fd8cc26e29d5cae9fc2fab9d
URL:		https://github.com/pickleshare/pickleshare
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pathlib2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests} && "%{py3_ver}" < "3.4"
BuildRequires:	python3-pathlib2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PickleShareDB object acts like a normal dictionary. Unlike shelve,
many processes can access the database simultaneously. Changing a
value in database is immediately visible to other processes accessing
the same database. Concurrency is possible because the values are
stored in separate files. Hence the "database" is a directory where
all files are governed by PickleShare.

%description -l pl.UTF-8
Obiekt PickleShareDB działa jak zwykły słownik. W przeciwieństwie do
shelve, wiele procesów może jednocześnie odwoływać się do bazy danych.
Zmiana wartości w bazie danych jest natychmiast widoczna dla innych
procesów odwołujących się do tej samej bazy. Współbieżność jest
możliwa, ponieważ wartości są zapisane w osobnych plikach. Stąd "baza
dnaych" to katalog, gdzie znajdują się wszystkie pliki utrzymywane
przez PickleShare.

%package -n python3-%{module}
Summary:	A small 'shelve' like datastore with concurrency support
Summary(pl.UTF-8):	Mały, podobny do 'shelve', zarządca danych z obsługą współbieżności
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
PickleShareDB object acts like a normal dictionary. Unlike shelve,
many processes can access the database simultaneously. Changing a
value in database is immediately visible to other processes accessing
the same database. Concurrency is possible because the values are
stored in separate files. Hence the "database" is a directory where
all files are governed by PickleShare.

%description -n python3-%{module} -l pl.UTF-8
Obiekt PickleShareDB działa jak zwykły słownik. W przeciwieństwie do
shelve, wiele procesów może jednocześnie odwoływać się do bazy danych.
Zmiana wartości w bazie danych jest natychmiast widoczna dla innych
procesów odwołujących się do tej samej bazy. Współbieżność jest
możliwa, ponieważ wartości są zapisane w osobnych plikach. Stąd "baza
dnaych" to katalog, gdzie znajdują się wszystkie pliki utrzymywane
przez PickleShare.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%{?with_tests:%{__python} -m pytest test_pickleshare.py}
%endif

%if %{with python3}
%py3_build

%{?with_tests:%{__python3} -m pytest test_pickleshare.py}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py_sitescriptdir}/pickleshare.py[co]
%{py_sitescriptdir}/pickleshare-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/pickleshare.py
%{py3_sitescriptdir}/__pycache__/pickleshare.cpython-*.pyc
%{py3_sitescriptdir}/pickleshare-%{version}-py*.egg-info
%endif

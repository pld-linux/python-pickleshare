# TODO:
# - fix tests

# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	pickleshare
Summary:	A small 'shelve' like datastore with concurrency support
Summary(pl.UTF-8):	Mały, podobny do 'shelve', zarządca danych z wsparciem dla konkurencyjności
Name:		python-%{module}
Version:	0.7.4
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/pickleshare/pickleshare/archive/%{version}.tar.gz
# Source0-md5:	edd1fc04bc12d9748c852218d2cb86fd
URL:		https://github.com/pickleshare/pickleshare
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
Requires:	python-pathlib2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PickleShareDB object acts like a normal dictionary. Unlike shelve,
many processes can access the database simultaneously. Changing a
value in database is immediately visible to other processes accessing
the same database. Concurrency is possible because the values are
stored in separate files. Hence the "database" is a directory where
all files are governed by PickleShare.

# %%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules
Requires:	python3-pathlib2


%description -n python3-%{module}
PickleShareDB object acts like a normal dictionary. Unlike shelve,
many processes can access the database simultaneously. Changing a
value in database is immediately visible to other processes accessing
the same database. Concurrency is possible because the values are
stored in separate files. Hence the "database" is a directory where
all files are governed by PickleShare.

# %%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}


%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

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
%doc README.md
%{py_sitescriptdir}/%{module}.py*
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.*.pyc


%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

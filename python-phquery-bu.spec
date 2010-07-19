%define pyname phquery
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: A simple module for getting info from a PH/QI server
Name: python-%{pyname}
Version: 0.4
Release: %{bu_tag}6
Source0: %{pyname}-%{version}.tar.gz
#Source9999: original BU package -- no upstream source
License: GPL
URL: http://www.mattdm.org/misc/python-py/
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
A simple module for getting info from a PH/QI server.

%prep
%setup -n %{pyname}-%{version}

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
python setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%ghost %{python_sitelib}/%{pyname}.pyo

%changelog
* Mon Apr 23 2007 Joe Szep <jszep@bu.edu> - 0.4-bu50s.6
- Fixed version tag from previous changelog entry
- bumped version number

* Thu Apr 19 2007 Joe Szep <jszep@bu.edu> - 0.4-bu45s.5
- port to Monde - using Zodiac package
- BU bug #6797

* Tue Aug 01 2006 Wesley Harrell <wesley@bu.edu> - 0.4-bu45s.4
- backport of stormy pkg
- see: http://lbugs.bu.edu/show_bug.cgi?id=6358

* Tue Jun 06 2006 Wesley Harrell <wesley@bu.edu> - 0.4-bu46.3
- Built with new fedora python .pyo file guidelines, see 6205

* Tue Jun 06 2006 Wesley Harrell <wesley@bu.edu> - 0.4-bu46.2
- Complete rewrite of code from allanonjl
- Built for Stormy
- see: http://lbugs.bu.edu/show_bug.cgi?id=6205

* Wed Mar 15 2006 Joe Szep <jszep@bu.edu> - 0.2-bu45.3
- port to Stormy, BU bug #5652

* Wed Mar  2 2005 Matthew Miller <mattdm@bu.edu> 0.2-bu45.3
- a little bit of code cleanup; decrease timeout.

* Wed Mar  2 2005 Matthew Miller <mattdm@bu.edu> 0.2-bu45.1
- pure python implementation -- the protocol isn't that hard, and
  all of the C libraries are unmaintained.

* Wed Jun  9 2004 Joe Szep <jszep@bu.edu> 0.1-bu40.3
- convention is to have a Source9999 line - adding...
- bumped release number to 3

* Fri Apr  9 2004 Matthew Miller <mattdm@bu.edu> 0.1-bu39.2
- update for Bossanova; minor spec file cleanup

* Fri Mar 14 2003 Matthew Miller <mattdm@mattdm.org> 0.1-bu1
- initial build

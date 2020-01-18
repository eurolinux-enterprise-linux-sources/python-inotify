%if 0%{?fedora}
%global with_python3 1
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

%global oname  pyinotify

Summary:       Monitor filesystem events with Python under Linux
Name:          python-inotify
Version:       0.9.4
Release:       4%{?dist}
License:       MIT
Group:         Development/Libraries
URL:           https://github.com/seb-m/pyinotify
Source0:       http://seb.dbzteam.org/pub/pyinotify/releases/pyinotify-%{version}.tar.gz
Source1:       %{oname}
BuildRequires: python-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a Python module for watching filesystems changes. pyinotify
can be used for various kind of fs monitoring. pyinotify relies on a
recent Linux Kernel feature (merged in kernel 2.6.13) called
inotify. inotify is an event-driven notifier, its notifications are
exported from kernel space to user space.

%package       examples
Summary:       Examples for Python inotify module
Group:         Development/Libraries
Requires:      python-inotify = %{version}-%{release}

%description   examples
This package includes some examples usage of the Python inotify module.

%if 0%{?with_python3}
%package -n    python3-inotify
Summary:       Monitor filesystem events with Python under Linux
Group:         Development/Languages

%description -n python3-inotify
This is a Python 3 module for watching filesystems changes. pyinotify
can be used for various kind of fs monitoring. pyinotify relies on a
recent Linux Kernel feature (merged in kernel 2.6.13) called
inotify. inotify is an event-driven notifier, its notifications are
exported from kernel space to user space.

This is the Python 3 build of pyinotify
%endif # if with_python3

%prep
%setup -q -n %{oname}-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__rm} -rf %{buildroot}

# Install python 3 first, so that python 2 gets precedence:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -D -m 0755 -p %{SOURCE1} %{buildroot}%{_bindir}/python3-%{oname}
%{__sed} -i -e 's/^python /python3 /' %{buildroot}%{_bindir}/python3-%{oname}
%{__chmod} 0755 %{buildroot}%{python3_sitelib}/%{oname}.py
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -D -m 0755 -p %{SOURCE1} %{buildroot}%{_bindir}/%{oname}
%{__chmod} 0755 %{buildroot}%{python_sitelib}/%{oname}.py

# examples
%{__install} -d -m 0755 %{buildroot}%{_datadir}/%{oname}
%{__cp} -a python2/examples/* %{buildroot}%{_datadir}/%{oname}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc ACKS COPYING README.md
%{_bindir}/%{oname}
%{python_sitelib}/%{oname}*

%files examples
%defattr(-, root, root, -)
%{_datadir}/%{oname}

%if 0%{?with_python3}
%files -n python3-inotify
%defattr(-, root, root, -)
%doc ACKS COPYING README.md
%{_bindir}/python3-%{oname}
%{python3_sitelib}/%{oname}*
%if 0%{?fedora} > 14
%{python3_sitelib}/__pycache__/%{oname}*
%endif
%endif

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.4-4
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Jakub Filak <jfilak@redhat.com> - 0.9.4-3
- make with_python3 be conditional on fedora

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.9.4-1
- 0.9.4

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.9.3-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.9.3-1
- 0.9.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 02 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.2-1
- 0.9.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.1-1
- 0.9.1

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.9.0-3
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jun 19 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.9.0-1
- 0.9.0
- Add python 3 subpackage
- License changed to MIT

* Sun Dec 06 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.8-1
- 0.8.8

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2.git20090518
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.6-1.git20090518
- Update to latest git, fixing bz #500934.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2.git20090208
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  8 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.1-1.git20090208
- 0.8.1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.0-4.r
- Rebuild for Python 2.6

* Sun Jun 22 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-3.r
- rebuild 

* Tue Jun 17 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-2.r
- 0.8.0r
- add wrapper in /usr/bin

* Mon Jun 16 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-1.q
- 0.8.0q
- Update url, license and source url

* Sat Feb  9 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.1-2
- Rebuild

* Wed Aug 08 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.1-1
- New upstream release: 0.7.1
- Fix license tag

* Mon Jun 25 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-3
- Remove autopath from example package (bz #237464)

* Tue Mar 27 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-2
- Fix email address

* Tue Mar  6 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-1
- Initial build


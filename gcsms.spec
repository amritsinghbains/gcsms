%define name    gcsms
%define version 2.3
%define release 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Send free SMS notification

Group:          Development/Libraries
License:        GPLv3
Source0:        %{name}-%{version}.tar.gz
Vendor:         Mansour Behabadi <mansour@oxplot.com>
URL:            https://github.com/oxplot/gcsms

BuildArch:      noarch
BuildRequires:  python >= 2.7
Requires:       python >= 2.7

%description
Send SMS for free through shell using Google Calendar API.

%prep
%setup -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.md LICENSE sample.config

%changelog
* Mon Oct 7 2013 Mansour Behabadi <mansour@oxplot.com> - 2.3-1
- Initial release

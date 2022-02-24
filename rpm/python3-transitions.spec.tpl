%global sum A lightweight, object-oriented finite state machine implementation in Python with many extensions
%global desc \
A lightweight, object-oriented state machine implementation in Python with many extensions. \
Compatible with Python 2.7+ and 3.0+.


Name:           python3-transitions
Version:        @VERSION@
Release:        @RELEASE@%{?dist}
Summary:        %{sum}

License:        MIT
URL:            https://github.com/pytransitions/transitions
Source0:        %{url}/archive/v%{version}/python3-transitions-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

%description
%{desc}

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n %{name}
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* @DATE@ Alexander Neumann <aleneum@gmail.com> - @VERSION@-@RELEASE@
- built from upstream, changelog ignored

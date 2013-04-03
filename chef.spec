# TODO
# - try not to use /var/chef
Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	0.10.6
Release:	0.4
License:	Apache v2.0
Group:		Development/Languages
URL:		http://wiki.opscode.com/display/chef
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	ea8746476a2ec37e1f8265a9febba6b9
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
Requires:	ruby >= 1:1.8.7
Requires:	ruby-bunny >= 0.6.0
Requires:	ruby-erubis
Requires:	ruby-mixlib-authentication >= 1.1.0
Requires:	ruby-mixlib-config >= 1.1.2
Requires:	ruby-mixlib-log >= 1.3.0
Requires:	ruby-moneta
Requires:	ruby-ohai >= 0.6
Requires:	ruby-rubygems
Requires:	ruby-uuidtools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rdoc
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/chef-client
%attr(755,root,root) %{_bindir}/chef-solo
%attr(755,root,root) %{_bindir}/knife
%attr(755,root,root) %{_bindir}/shef
%{ruby_rubylibdir}/chef.rb
%{ruby_rubylibdir}/chef

# FIXME: FHS
%dir /var/%{name}

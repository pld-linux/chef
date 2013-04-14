# TODO
# - try not to use /var/chef
Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	11.4.0
Release:	0.4
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	1ebabd6fdeae44a99d5cb199c38adc15
URL:		http://wiki.opscode.com/display/chef
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
Requires:	ruby >= 1:1.8.7
Requires:	ruby-erubis
Requires:	ruby-highline >= 1.6.9
Requires:	ruby-json <= 1.7.7
Requires:	ruby-json >= 1.4.4
Requires:	ruby-mixlib-authentication >= 1.3.0
Requires:	ruby-mixlib-cli >= 1.3.0
Requires:	ruby-mixlib-config >= 1.1.2
Requires:	ruby-mixlib-log >= 1.3.0
Requires:	ruby-mixlib-shellout
Requires:	ruby-net-ssh >= 2.6
Requires:	ruby-net-ssh-multi >= 1.1.0
Requires:	ruby-ohai >= 0.6.0
Requires:	ruby-rest-client < 1.7.0
Requires:	ruby-rest-client >= 1.0.4
Requires:	ruby-rubygems
Requires:	ruby-yajl >= 1.1
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
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/chef-apply
%attr(755,root,root) %{_bindir}/chef-client
%attr(755,root,root) %{_bindir}/chef-shell
%attr(755,root,root) %{_bindir}/chef-solo
%attr(755,root,root) %{_bindir}/knife
%attr(755,root,root) %{_bindir}/shef
%{ruby_rubylibdir}/chef.rb
%{ruby_rubylibdir}/chef

# FIXME: FHS
%dir /var/%{name}

Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	11.4.4
Release:	0.12
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	dc50aa6a4a7d4785a4c82fcaab3f9436
Patch0:		platform-pld.patch
Patch1:		FHS.patch
URL:		http://wiki.opscode.com/display/chef
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rack
BuildRequires:	ruby-rake
BuildRequires:	ruby-rdoc
BuildRequires:	ruby-rspec-core >= 2.12.0
BuildRequires:	ruby-rspec-expectations >= 2.12.0
BuildRequires:	ruby-rspec-mocks >= 2.12.0
BuildRequires:	ruby-rspec_junit_formatter
BuildRequires:	ruby-sdoc
%endif
Requires:	lsb-release
Requires:	ruby-erubis
Requires:	ruby-highline >= 1.6.9
Requires:	ruby-json >= 1.4.4
Requires:	ruby-mixlib-authentication >= 1.3.0
Requires:	ruby-mixlib-cli >= 1.3.0
Requires:	ruby-mixlib-config >= 1.1.2
Requires:	ruby-mixlib-log >= 1.3.0
Requires:	ruby-mixlib-shellout
Requires:	ruby-net-ssh >= 2.6
Requires:	ruby-net-ssh-multi >= 1.1.0
Requires:	ruby-ohai >= 0.6.0
Requires:	ruby-rest-client >= 1.0.4
Requires:	ruby-rubygems
Requires:	ruby-yajl >= 1.1
Requires:	yum >= 3.4.3-7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/var/{cache,lib}}/%{name}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}


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
%{ruby_vendorlibdir}/chef.rb
%{ruby_vendorlibdir}/chef

%dir /var/lib/%{name}
%dir /var/cache/%{name}

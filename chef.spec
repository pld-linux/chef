#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	11.6.2
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	8db9eb4b3c75be30e8125ea4eedd3f01
Source1:	%{name}.rb
Source2:	%{name}.tmpfiles
Patch0:		platform-pld.patch
Patch1:		FHS.patch
Patch2:		https://github.com/glensc/chef/compare/poldek.patch
# Patch2-md5:	5a0fc35de33910b41cba4e87dcb4bf9a
Patch3:		https://github.com/glensc/chef/compare/pld-knife-boostrap.patch
# Patch3-md5:	bfc884469fad7b5aa46341402be5fccd
URL:		http://wiki.opscode.com/display/chef
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-abstract
BuildRequires:	ruby-chef-zero < 2
BuildRequires:	ruby-chef-zero >= 1.4
BuildRequires:	ruby-mixlib-authentication >= 1.3.0
BuildRequires:	ruby-net-ssh-multi >= 1.1.0
BuildRequires:	ruby-puma < 2
BuildRequires:	ruby-puma >= 1.6
BuildRequires:	ruby-rack
BuildRequires:	ruby-rake
#BuildRequires:	ruby-rdoc
BuildRequires:	ruby-rest-client >= 1.0.4
BuildRequires:	ruby-rspec-core >= 2.12.0
BuildRequires:	ruby-rspec-expectations >= 2.12.0
BuildRequires:	ruby-rspec-mocks >= 2.12.0
#BuildRequires:	ruby-rspec_junit_formatter
#BuildRequires:	ruby-sdoc
%endif
Requires:	lsb-release
Requires:	poldek >= 0.30
Requires:	ruby >= 1:1.9.3.429-4
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
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# do not generate python dependency, yum support is optional
%define		_noautoreqfiles %{ruby_vendorlibdir}/chef/provider/package/yum-dump.py

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

grep --exclude-dir=spec --exclude-dir=distro -r /var/chef . && exit 1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
%if %{with tests}
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir},%{_mandir}/man1,%{systemdtmpfilesdir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/var/{run/%{name},cache/%{name},lib/%{name}/{roles,data_bags,environments}}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a distro/common/man/* $RPM_BUILD_ROOT%{_mandir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/chef.rb
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/chef.rb
%attr(755,root,root) %{_bindir}/chef-apply
%attr(755,root,root) %{_bindir}/chef-client
%attr(755,root,root) %{_bindir}/chef-service-manager
%attr(755,root,root) %{_bindir}/chef-shell
%attr(755,root,root) %{_bindir}/chef-solo
%attr(755,root,root) %{_bindir}/knife
%attr(755,root,root) %{_bindir}/shef
%{_mandir}/man1/chef-shell.1*
%{_mandir}/man1/knife-bootstrap.1*
%{_mandir}/man1/knife-client.1*
%{_mandir}/man1/knife-configure.1*
%{_mandir}/man1/knife-cookbook-site.1*
%{_mandir}/man1/knife-cookbook.1*
%{_mandir}/man1/knife-data-bag.1*
%{_mandir}/man1/knife-environment.1*
%{_mandir}/man1/knife-exec.1*
%{_mandir}/man1/knife-index.1*
%{_mandir}/man1/knife-node.1*
%{_mandir}/man1/knife-role.1*
%{_mandir}/man1/knife-search.1*
%{_mandir}/man1/knife-ssh.1*
%{_mandir}/man1/knife-status.1*
%{_mandir}/man1/knife-tag.1*
%{_mandir}/man1/knife.1*
%{_mandir}/man8/chef-client.8*
%{_mandir}/man8/chef-expander.8*
%{_mandir}/man8/chef-expanderctl.8*
%{_mandir}/man8/chef-server-webui.8*
%{_mandir}/man8/chef-server.8*
%{_mandir}/man8/chef-solo.8*
%{_mandir}/man8/chef-solr.8*
%{ruby_vendorlibdir}/chef.rb
%{ruby_vendorlibdir}/chef
%{systemdtmpfilesdir}/chef.conf

%dir /var/lib/%{name}
%dir /var/lib/%{name}/roles
%dir /var/lib/%{name}/data_bags
%dir /var/lib/%{name}/environments

%dir /var/cache/%{name}
%dir /var/run/%{name}

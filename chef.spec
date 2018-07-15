# NOTE:
# - check releases here: https://github.com/opscode/chef/releases

# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	14.1.21
Release:	3
License:	Apache v2.0
Group:		Networking/Admin
Source0:	https://github.com/chef/chef/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b67966a9b9e6c0a5947a604239267415
Source2:	%{name}.tmpfiles
Source3:	https://raw.github.com/stevendanna/knife-hacks/master/shell/knife_completion.sh
# Source3-md5:	a4c1e41370be8088a59ddb3b2e7ea397
Patch0:		platform-pld.patch
Patch1:		FHS.patch
Patch2:		poldek.patch
Patch3:		https://github.com/glensc/chef/compare/pld-knife-boostrap.patch
# Patch3-md5:	9bc4b39952e6bc326b16207cd6a59141
Patch4:		optional-plist.patch
URL:		https://www.chef.io/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rack
BuildRequires:	ruby-rake
BuildRequires:	ruby-rspec-core < 2.15
BuildRequires:	ruby-rspec-core >= 2.14.0
BuildRequires:	ruby-rspec-expectations < 2.15
BuildRequires:	ruby-rspec-expectations >= 2.14.0
BuildRequires:	ruby-rspec-mocks < 2.15
BuildRequires:	ruby-rspec-mocks >= 2.14.0
BuildRequires:	ruby-rspec_junit_formatter
%endif
Requires:	lsb-release
Requires:	poldek >= 0.30
Requires:	ruby >= 1:2.4.0
Requires:	ruby-addressable >= 0
Requires:	ruby-bundler >= 1.10
Requires:	ruby-chef-config = %{version}
Requires:	ruby-diff-lcs >= 1.2.4
Requires:	ruby-diff-lcs < 2
Requires:	ruby-erubis >= 2.7.0-3
Requires:	ruby-erubis < 3
Requires:	ruby-ffi >= 1.9.22
Requires:	ruby-ffi < 2
Requires:	ruby-ffi-yajl >= 2.2
Requires:	ruby-ffi-yajl < 3
Requires:	ruby-highline >= 1.6.9
Requires:	ruby-highline < 2
Requires:	ruby-iniparse >= 1.4
Requires:	ruby-iniparse < 2
Requires:	ruby-iso8601 >= 0.9.1
Requires:	ruby-iso8601 < 0.10
Requires:	ruby-mixlib-archive >= 0.4
Requires:	ruby-mixlib-archive < 1
Requires:	ruby-mixlib-authentication >= 2.0
Requires:	ruby-mixlib-authentication < 3
Requires:	ruby-mixlib-cli >= 1.7
Requires:	ruby-mixlib-cli < 2
Requires:	ruby-mixlib-log >= 2.0.3
Requires:	ruby-mixlib-log < 3
Requires:	ruby-mixlib-shellout >= 2.0
Requires:	ruby-mixlib-shellout < 3
Requires:	ruby-net-sftp >= 2.1.2
Requires:	ruby-net-sftp < 3
Requires:	ruby-net-ssh >= 4.2
Requires:	ruby-net-ssh-multi >= 1.2.1
Requires:	ruby-net-ssh-multi < 2
Requires:	ruby-ohai >= 14.0
Requires:	ruby-ohai < 15
Requires:	ruby-proxifier >= 1.0
Requires:	ruby-proxifier < 2
Requires:	ruby-rspec-core >= 3.5
Requires:	ruby-rspec-core < 4
Requires:	ruby-rspec-expectations >= 3.5
Requires:	ruby-rspec-expectations < 4
Requires:	ruby-rspec_junit_formatter >= 0.2.0
Requires:	ruby-rspec-mocks >= 3.5
Requires:	ruby-rspec-mocks < 4
Requires:	ruby-rubygems
Requires:	ruby-serverspec >= 2.7
Requires:	ruby-serverspec < 3
Requires:	ruby-specinfra >= 2.10
Requires:	ruby-specinfra < 3
Requires:	ruby-syslog-logger >= 1.6
Requires:	ruby-syslog-logger < 2
Requires:	ruby-uuidtools >= 2.1.5
Requires:	ruby-uuidtools < 2.2
Suggests:	chef-zero >= 13.0
Suggests:	ruby-plist >= 3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# do not generate python dependency, yum support is optional
%define		_noautoreqfiles %{ruby_vendorlibdir}/chef/provider/package/yum-dump.py

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%package -n bash-completion-knife
Summary:	bash-completion for knife
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla knifea
Group:		Applications/Shells
Requires:	%{name} >= 0.10
Requires:	bash-completion >= 2.0

%description -n bash-completion-knife
This package provides bash-completion for knife.

%description -n bash-completion-knife -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla knifea.

%package -n knife
Summary:	knife - Chef Server API client utility
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}

%description -n knife
Knife is a command-line utility used to manage data on a Chef server
through the HTTP(S) API. Knife is organized into groups of subcommands
centered around the various object types in Chef. Each category of
subcommand is documented in its own manual page.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

#grep --exclude-dir=spec --exclude-dir=distro -r /var/chef . && exit 1

%build
%if %{with tests}
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_bindir},%{_mandir}/man1,%{systemdtmpfilesdir}} \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/chef/reporting \
	$RPM_BUILD_ROOT/var/{run/%{name},cache/%{name},lib/%{name}/{roles,data_bags,environments,backup}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{bash_compdir}/knife

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/chef-apply
%attr(755,root,root) %{_bindir}/chef-client
%attr(755,root,root) %{_bindir}/chef-resource-inspector
%attr(755,root,root) %{_bindir}/chef-service-manager
%attr(755,root,root) %{_bindir}/chef-shell
%attr(755,root,root) %{_bindir}/chef-solo
%attr(755,root,root) %{_bindir}/chef-windows-service
%{ruby_vendorlibdir}/chef.rb
%{ruby_vendorlibdir}/chef
%exclude %{ruby_vendorlibdir}/chef/knife
%exclude %{ruby_vendorlibdir}/chef/application/knife.rb
%exclude %{ruby_vendorlibdir}/chef/chef_fs/knife.rb
%exclude %{ruby_vendorlibdir}/chef/knife.rb
%{systemdtmpfilesdir}/chef.conf

%dir /var/lib/%{name}
%dir /var/lib/%{name}/roles
%dir /var/lib/%{name}/data_bags
%dir /var/lib/%{name}/environments
%dir %attr(750,root,root) /var/lib/%{name}/backup

%dir /var/cache/%{name}
%dir /var/run/%{name}

%files -n knife
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/knife
%{ruby_vendorlibdir}/chef/knife.rb
%{ruby_vendorlibdir}/chef/knife
%{ruby_vendorlibdir}/chef/application/knife.rb
%{ruby_vendorlibdir}/chef/chef_fs/knife.rb

%files -n bash-completion-knife
%defattr(644,root,root,755)
%{bash_compdir}/knife

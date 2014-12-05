# NOTE:
# - check releases here: https://github.com/opscode/chef/releases

# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	11.14.6
Release:	1
License:	Apache v2.0
Group:		Networking/Admin
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	0a7dbf9c3b7b9e285de034031faf008f
Source1:	%{name}.rb
Source2:	%{name}.tmpfiles
Source3:	https://raw.github.com/stevendanna/knife-hacks/master/shell/knife_completion.sh
# Source3-md5:	a4c1e41370be8088a59ddb3b2e7ea397
Patch0:		platform-pld.patch
Patch1:		FHS.patch
Patch2:		poldek.patch
Patch3:		https://github.com/glensc/chef/compare/pld-knife-boostrap.patch
# Patch3-md5:	8ff0fdfde6dc90018698775bf8f13062
URL:		https://wiki.opscode.com/display/chef/
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
Requires:	ruby >= 1:1.9.3.429-4
Requires:	ruby-diff-lcs < 2
Requires:	ruby-diff-lcs >= 1.2.4
Requires:	ruby-erubis < 3
Requires:	ruby-erubis >= 2.7.0-3
Requires:	ruby-highline < 2
Requires:	ruby-highline >= 1.6.9
Requires:	ruby-json <= 1.8.1
Requires:	ruby-json >= 1.4.4
Requires:	ruby-mime-types < 2
Requires:	ruby-mime-types >= 1.16
Requires:	ruby-mixlib-authentication < 2
Requires:	ruby-mixlib-authentication >= 1.3.0-2
Requires:	ruby-mixlib-cli < 2
Requires:	ruby-mixlib-cli >= 1.4
Requires:	ruby-mixlib-config < 3
Requires:	ruby-mixlib-config >= 2.0
Requires:	ruby-mixlib-log < 2
Requires:	ruby-mixlib-log >= 1.6.0-2
Requires:	ruby-mixlib-shellout >= 1.4
Requires:	ruby-net-ssh < 3
Requires:	ruby-net-ssh >= 2.6
Requires:	ruby-net-ssh-multi < 2
Requires:	ruby-net-ssh-multi >= 1.1
Requires:	ruby-ohai < 8
Requires:	ruby-ohai >= 6.0
Requires:	ruby-rest-client < 1.7.0
Requires:	ruby-rest-client >= 1.0.4
Requires:	ruby-rubygems
Requires:	ruby-yajl < 2
Requires:	ruby-yajl >= 1.1
Suggests:	chef-zero >= 2.0
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
gzip -d metadata
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

grep --exclude-dir=spec --exclude-dir=distro -r /var/chef . && exit 1

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
cp -a distro/common/man/* $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/README.md

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/chef.rb
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{bash_compdir}/knife

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
%attr(755,root,root) %{_bindir}/shef
%{_mandir}/man1/chef-shell.1*
%{_mandir}/man8/chef-client.8*
%{_mandir}/man8/chef-solo.8*
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
%{_mandir}/man1/knife-bootstrap.1*
%{_mandir}/man1/knife-client.1*
%{_mandir}/man1/knife-configure.1*
%{_mandir}/man1/knife-cookbook-site.1*
%{_mandir}/man1/knife-cookbook.1*
%{_mandir}/man1/knife-data-bag.1*
%{_mandir}/man1/knife-delete.1*
%{_mandir}/man1/knife-deps.1*
%{_mandir}/man1/knife-diff.1*
%{_mandir}/man1/knife-download.1*
%{_mandir}/man1/knife-edit.1*
%{_mandir}/man1/knife-environment.1*
%{_mandir}/man1/knife-exec.1*
%{_mandir}/man1/knife-index-rebuild.1*
%{_mandir}/man1/knife-list.1*
%{_mandir}/man1/knife-node.1*
%{_mandir}/man1/knife-raw.1*
%{_mandir}/man1/knife-recipe-list.1*
%{_mandir}/man1/knife-role.1*
%{_mandir}/man1/knife-search.1*
%{_mandir}/man1/knife-serve.1*
%{_mandir}/man1/knife-show.1*
%{_mandir}/man1/knife-ssh.1*
%{_mandir}/man1/knife-ssl-check.1*
%{_mandir}/man1/knife-ssl-fetch.1*
%{_mandir}/man1/knife-status.1*
%{_mandir}/man1/knife-tag.1*
%{_mandir}/man1/knife-upload.1*
%{_mandir}/man1/knife-user.1*
%{_mandir}/man1/knife-xargs.1*
%{_mandir}/man1/knife.1*

%files -n bash-completion-knife
%defattr(644,root,root,755)
%{bash_compdir}/knife

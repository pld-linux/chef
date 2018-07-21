# NOTE:
# - check releases here: https://downloads.chef.io/chef-client/debian/
#   the versions tagged in github are somewhat newer, perhaps dev-releases

# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	14.1.36
Release:	0.8
License:	Apache v2.0
Group:		Networking/Admin
Source0:	https://github.com/chef/chef/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	442169a1a824b3335376a88723e133a0
Source2:	%{name}.tmpfiles
Source3:	https://raw.github.com/stevendanna/knife-hacks/master/shell/knife_completion.sh
# Source3-md5:	a4c1e41370be8088a59ddb3b2e7ea397
Patch0:		platform-pld.patch
Patch1:		FHS.patch
Patch2:		poldek.patch
Patch3:		https://github.com/glensc/chef/compare/pld-knife-boostrap.patch
# Patch3-md5:	8ff0fdfde6dc90018698775bf8f13062
Patch4:		optional-plist.patch
Patch5:		gemdeps.patch
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
Requires:	ruby >= 1:1.9.3.429-4
Requires:	ruby-chef-config = %{version}-%{release}
Requires:	ruby-erubis >= 2.7.0-3
Requires:	ruby-json
Requires:	ruby-mime-types < 2
Requires:	ruby-mime-types >= 1.16
Requires:	ruby-mixlib-config < 3
Requires:	ruby-mixlib-config >= 2.0
Requires:	ruby-rest-client >= 1.0.4
Requires:	ruby-rubygems
Suggests:	chef-zero >= 2.1.4
Suggests:	ruby-plist >= 3.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# do not generate python dependency, yum support is optional
%define		_noautoreqfiles %{ruby_vendorlibdir}/chef/provider/package/yum-dump.py

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%package -n ruby-chef-config
Summary:	Chef's default configuration and config loading
Group:		Development/Languages

%description -n ruby-chef-config
Chef's default configuration and config loading.

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
%patch5 -p1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%ifos linux
# those do not match s.executables from .gemspec
rm bin/chef-service-manager
rm bin/chef-windows-service
%endif

# don't package this, a maintainer's rake task
rm chef-config/lib/chef-config/package_task.rb

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

grep --exclude-dir=spec --exclude-dir=distro --exclude=CHANGELOG.md -r /var/chef . && exit 1

%build
# make gemspec self-contained
%__gem_helper spec-dump %{name}.gemspec

%if %{with tests}
rspec spec
%endif

cd chef-config
# make gemspec self-contained
%__gem_helper spec-dump %{name}-config.gemspec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_bindir},%{systemdtmpfilesdir}} \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/chef/reporting \
	$RPM_BUILD_ROOT%{ruby_specdir} \
	$RPM_BUILD_ROOT/var/{run/%{name},cache/%{name},lib/%{name}/{roles,data_bags,environments,reports,backup}}

# chef
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p chef-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

# chef-config
cp -a chef-config/lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p chef-config/chef-config-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

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
%attr(755,root,root) %{_bindir}/chef-shell
%attr(755,root,root) %{_bindir}/chef-solo
%{ruby_vendorlibdir}/chef.rb
%{ruby_vendorlibdir}/chef
%{ruby_specdir}/chef-%{version}.gemspec
%exclude %{ruby_vendorlibdir}/chef/knife
%exclude %{ruby_vendorlibdir}/chef/application/knife.rb
%exclude %{ruby_vendorlibdir}/chef/chef_fs/knife.rb
%exclude %{ruby_vendorlibdir}/chef/knife.rb
%{systemdtmpfilesdir}/chef.conf

%dir /var/lib/%{name}
%dir /var/lib/%{name}/roles
%dir /var/lib/%{name}/data_bags
%dir /var/lib/%{name}/environments
%dir /var/lib/%{name}/reports
%dir %attr(750,root,root) /var/lib/%{name}/backup

%dir /var/cache/%{name}
%dir /var/run/%{name}

%files -n ruby-chef-config
%defattr(644,root,root,755)
%{ruby_vendorlibdir}/chef-config.rb
%{ruby_vendorlibdir}/chef-config
%{ruby_specdir}/chef-config-%{version}.gemspec

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

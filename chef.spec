Summary:	A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name:		chef
Version:	0.10.6
Release:	0.2
License:	Apache v2.0
Group:		Development/Languages
URL:		http://wiki.opscode.com/display/chef
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	ea8746476a2ec37e1f8265a9febba6b9
BuildRequires:	rubygems
Requires:	ruby >= 1:1.8.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A systems integration framework, built to bring the benefits of
configuration management to your entire infrastructure.

%prep
%setup -qc
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README.rdoc -o -print | xargs touch --reference %{SOURCE0}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

%files
%defattr(644,root,root,755)
%doc README.rdoc
%attr(755,root,root) %{_bindir}/chef-client
%attr(755,root,root) %{_bindir}/chef-solo
%attr(755,root,root) %{_bindir}/knife
%attr(755,root,root) %{_bindir}/shef
%{ruby_rubylibdir}/chef.rb
%{ruby_rubylibdir}/chef

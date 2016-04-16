%define gitlab_user  git
%define gitlab_group git
%define gitlab_gid 264
%define gitlab_uid 264
Summary:	Just some shared directories and users
Name:		gitlab-common
Version:	8.6
Release:	0.1
License:	MIT
Group:		Base
BuildRequires:	rpmbuild(macros) >= 1.202
Provides:	group(%{gitlab_group})
Provides:	user(%{gitlab_user})
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define git_dir          /srv/gitlab
%define satellites_dir   %{git_dir}/satellites
%define repositories_dir %{git_dir}/repositories
%define build_dir        %{git_dir}/builds
%define shared_dir       %{git_dir}/shared
%define home_dir         %{git_dir}

%description
Just some shared directories and users for gitlab shell and webapp.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{satellites_dir} \
	$RPM_BUILD_ROOT%{repositories_dir} \
	$RPM_BUILD_ROOT%{build_dir} \
	$RPM_BUILD_ROOT%{shared_dir} \
	$RPM_BUILD_ROOT%{git_dir}/.ssh

touch $RPM_BUILD_ROOT%{git_dir}/.ssh/authorized_keys
chmod -R u=rwX,g=rX,o= $RPM_BUILD_ROOT%{git_dir}
chmod -R go= $RPM_BUILD_ROOT%{git_dir}/.ssh

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g %{gitlab_gid} -r %{gitlab_group}
%useradd -u %{gitlab_uid} -g %{gitlab_group} -s /bin/sh -r -c "GitLab" -d %{home_dir} %{gitlab_user}

%files
%defattr(644,root,root,755)
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{git_dir}
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{build_dir}
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{repositories_dir}
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{satellites_dir}
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{shared_dir}
%dir %attr(-,%{gitlab_user},%{gitlab_group}) %{git_dir}/.ssh
%config(noreplace) %verify(not md5 mtime size) %attr(-,%{gitlab_user},%{gitlab_group}) %{git_dir}/.ssh/authorized_keys

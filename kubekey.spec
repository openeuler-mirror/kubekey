%define debug_package %{nil}

Name:        kubekey
Summary:     The Next-gen Installer: Installing Kubernetes and KubeSphere v3.0.0 and v2.1.1 fastly, flexibly and easily
Version:     2.1.1
Release:     1%{?dist}
License:     Apache 2.0
URL:         https://github.com/kubesphere/kubekey
BuildArch:   aarch64

Source0:     kubekey.tar.gz

Requires:   socat
Requires:   conntrack

Provides: kubekey = %{version}

%description

%prep
%setup

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/usr/local/kubekey
cp kk.sh $RPM_BUILD_ROOT%{_bindir}/kk
cp kk    $RPM_BUILD_ROOT/usr/local/kubekey

%files
%{_bindir}/kk
/usr/local/kubekey/

%changelog
* Fri Sep 4 2020 fuchangjie <fu_changjie@qq.com> 2.1.1-1
- Init package

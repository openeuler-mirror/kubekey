%define debug_package %{nil}

Name:        kubekey
Summary:     The Next-gen Installer: Installing Kubernetes and KubeSphere v3.0.0 and v2.1.1 fastly, flexibly and easily
Version:     2.1.1
Release:     2%{?dist}
License:     Apache 2.0
URL:         https://gitee.com/openeuler/kubekey
BuildArch:   aarch64

Source0:     kubekey.tar.gz

BuildRequires:	golang >= 1.13
BuildRequires:  git
Requires:   	socat
Requires:   	conntrack

Provides: kubekey = %{version}

%description

%prep
%setup

%build
bash -x build.sh

%install
mkdir -p $RPM_BUILD_ROOT/usr/local/kubekey
cp output/kk $RPM_BUILD_ROOT/usr/local/kubekey

%files
/usr/local/kubekey/

%post 
echo 'export PATH="$PATH:/usr/local/kubekey/"' >> /etc/profile
source /etc/profile

%preun
sed -i '/usr\/local\/kubekey\/\"$/d' /etc/profile

%changelog
* Thu Nov 26 2020 fuchangjie <fu_changjie@qq.com> 2.1.1-2
- 更换源文件为源码，而不是编译后的二进制文件

* Fri Sep 4 2020 fuchangjie <fu_changjie@qq.com> 2.1.1-1
- Init package

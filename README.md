# KubeKey

KubeKey 是基于 Go 语言开发的安装程序。使用 KubeKey，您可以轻松、高效、灵活地单独或整体安装 Kubernetes 和 KubeSphere。

此仓库为 KubeKey 在 ARM64v8 架构下的 opeEnuler 发行版特制 rpm 源码仓库。

## <span id = "KubernetesVersions">支持的 Kubernetes 版本</span> 

* **v1.15**: &ensp; *v1.15.12* (默认)

> * 后续将支持更多版本

## <span id = "KubeSphereVersions">支持的 KubeSphere 版本</span> 

* **v2.1.1**: &ensp; *v2.1.1* (默认)

> * 后续将支持更多版本

## 要求和建议

* 最低资源要求（仅对于最小安装 KubeSphere）：
  * 2 核虚拟 CPU
  * 4 GB 内存
  * 20 GB 储存空间

> /var/lib/docker 主要用于存储容器数据，在使用和操作过程中会逐渐增大。对于生产环境，建议 /var/lib/docker 单独挂盘。

* 操作系统要求：
  * `SSH` 可以访问所有节点。
  * 所有节点的时间同步。
  * `sudo`/`curl`/`openssl` 应在所有节点使用。
  * `docker` 可以自己安装，也可以通过 KubeKey 安装。
  * `Red Hat` 在其 `Linux` 发行版本中包括了`SELinux`，建议[关闭SELinux](./docs/turn-off-SELinux_zh-CN.md)或者将[SELinux的模式切换](./docs/turn-off-SELinux_zh-CN.md)为Permissive[宽容]工作模式

> * 建议您的操作系统环境足够干净 (不安装任何其他软件)，否则可能会发生冲突。
> * 默认情况下，KubeKey 将安装 [OpenEBS](https://openebs.io/) 来为开发和测试环境配置 LocalPV，这对新用户来说非常方便。对于生产，请使用 NFS/Ceph/GlusterFS 或商业化存储作为持久化存储，并在所有节点中安装[相关的客户端](./docs/storage-client.md) 。
> * 如果遇到拷贝时报权限问题Permission denied,建议优先考虑查看[SELinux的原因](./docs/turn-off-SELinux_zh-CN.md)。

* 网络和 DNS 要求：
  * 确保 `/etc/resolv.conf` 中的 DNS 地址可用。否则，可能会导致群集中出现某些 DNS 问题。
  * 如果您的网络配置使用防火墙或安全组，则必须确保基础结构组件可以通过特定端口相互通信。建议您关闭防火墙或遵循链接配置：[网络访问](docs/network-access.md)。

## 用法

### 获取 `kk` 命令

* 安装 KubeKey 的 rpm 包
> 由于暂时还未加入到 openEuler 仓库，需要本地编译成包
  安装后可直接使用 `kk` 命令。

### 创建集群

#### 快速开始

使用 `all-in-one` 安装，这是熟悉 KubeSphere 的良好开始。

##### 命令

```shell script
./kk create cluster [--with-kubernetes version] [--with-kubesphere version]
```

##### 例子

* 使用默认版本创建一个纯 Kubernetes 集群

    ```shell script
    ./kk create cluster
    ```

* 创建指定一个（[支持的版本](#KubernetesVersions)）的 Kubernetes 集群

    ```shell script
    ./kk create cluster --with-kubernetes v1.15.12
    ```

* 创建一个部署了 KubeSphere 的 Kubernetes 集群 （[支持的版本](#KubeSphereVersions), 例如 `--with-kubesphere v2.1.1`）

    ```shell script
    ./kk create cluster --with-kubesphere [version]
    ```

#### 高级用法

您可以使用配置文件来控制自定义参数或创建多节点群集。具体来说，通过指定配置文件来创建集群。

1. 首先，创建一个示例配置文件

    ```shell script
    kk create config [--with-kubernetes version] [--with-kubesphere version] [(-f | --file) path]
    ```

   **例子：**

   * 使用默认配置创建一个示例配置文件。您也可以指定文件名称或文件所在的文件夹。

        ```shell script
        kk create config [-f ~/myfolder/config-sample.yaml]
        ```

   * 同时安装 KubeSphere

        ```shell script
        kk create config --with-kubesphere
        ```

2. 根据您的环境修改配置文件 config-sample.yaml
> * 当指定安装KubeSphere时，要求集群中有可用的持久化存储。默认使用localVolume，如果需要使用其他持久化存储，请参阅 [addons](./docs/addons.md) 配置。
3. 使用配置文件创建集群。

      ```shell script
      kk create cluster -f ~/myfolder/config-sample.yaml
      ```

### 开启可插拔功能组件

KubeSphere 从 2.1.0 版本开始对 Installer 的各功能组件进行了解耦，快速安装将默认仅开启最小化安装（Minimal Installation），Installer 支持在安装前或安装后自定义可插拔的功能组件的安装。使最小化安装更快速轻量且资源占用更少，也方便不同用户按需选择安装不同的功能组件。

KubeSphere 有多个可插拔功能组件，功能组件的介绍可参考 [配置示例](docs/config-example.md)。您可以根据需求，选择开启安装 KubeSphere 的可插拔功能组件。我们非常建议您开启这些功能组件来体验 KubeSphere 完整的功能以及端到端的解决方案。请在安装前确保您的机器有足够的 CPU 与内存资源。开启可插拔功能组件可参考 [开启可选功能组件](https://github.com/kubesphere/ks-installer/blob/master/README_zh.md#%E5%AE%89%E8%A3%85%E5%8A%9F%E8%83%BD%E7%BB%84%E4%BB%B6)。

### 添加节点

将新节点的信息添加到群集配置文件，然后应用更改。

```shell script
kk add nodes -f config-sample.yaml
```
### 删除节点

通过以下命令删除节点，nodename指需要删除的节点名。

```shell script
kk delete node <nodeName> -f config-sample.yaml
```

### 删除集群

您可以通过以下命令删除集群：

* 如果您以快速入门（all-in-one）开始：

```shell script
./kk delete cluster
```

* 如果从高级安装开始（使用配置文件创建的集群）：

```shell script
./kk delete cluster [-f config-sample.yaml]
```

### 启用 kubectl 自动补全

KubeKey 不会启用 kubectl 自动补全功能。请参阅下面的指南并将其打开：

**先决条件**：确保已安装 `bash-autocompletion` 并可以正常工作。

```shell script
# 安装 bash-completion
yum install bash-completion

# 将 completion 脚本添加到你的 ~/.bashrc 文件
echo 'source <(kubectl completion bash)' >>~/.bashrc

# 将 completion 脚本添加到 /etc/bash_completion.d 目录
kubectl completion bash >/etc/bash_completion.d/kubectl
```

更详细的参考可以在[这里](https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion)找到。

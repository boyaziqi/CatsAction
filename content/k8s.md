title: Kubernetes系列一
subtitle: 原理和基本概念
date: 2019-01-24
category: Kubernetes
tags: k8s, docker

Kubernetes 是一个跨主机集群的，开源的容器调度平台。它可以自动化应用容器的部署、扩展和操作，提供以容器为中心的基础架构。
使用 Kubernetes，您可以快速高效地响应客户需求。
#### Kubernetes 特点
- 便携式，可扩展，自修复
- 服务发现和负载均衡
- 方便挂载外部存储
- 支持自检和调试
- 应用健康检测

#### Kubernetes 组成结构

![Kubernetes内部结构]({static}/images/components-of-kubernetes.png)

##### Master
Master 节点是整个集群控制的中心。负责集群的调度和 Pod 添加等事件的处理。Master 可以运行在集群中的任何一台机器上，但通常做法只在同一台机器启动 Master，而且这台机器专职运行 Master，而不运行用户容器。
>
- kube-apiserver，是控制中心开放的 API，Kubernetes 里资源操控和集群控制的入口进程。
- etcd，是 Kubernetes 的后端存储系统，所有数据都存储在这里。
- kube-scheduler 负责基于各种软硬件资源需求调度 Pod。
- cloud-controller-manager，用于与底层云提供商交互的控制器。

##### Node
Node 节点维护运行的 Pod 并提供 Kubernetes 运行时环境。
>
- kubelet，Node 节点的代理，负责容器创建、暂停等任务。提供各种机制保证容器运行和健康检测。
- kube-proxy，Kubernetes service 的通信与负载均衡机制的重要组件。

#### RabbitMQ 业务概念
##### Pods
最小部署单元，可包含多个容器，是连接在一起的容器组合并共享 Volume。它们是最小的部署单元，由 Kubernetes 统一创建、调度、管理。Pods是可以直接创建的，但推荐的做法是使用 Replication Controller，即使是创建一个 Pod。
![pods]({static}/images/k8s_pod.svg)

##### Labels
Label 以 key/value 形式附加到 Pos、Service、RC、Node 等上面，每个对象可以定义多个 label，以提供 Label Selector 来选择对象。

##### Replication Controller
管理 Pods 的生命周期。它们确保指定数量的 Pods 会一直运行，还有实现资源伸缩。

##### Deployment
1.2引入，为了更好地解决 pod 的编排问题，内部使用了 Replica Set 实现；它相对于RC的最大的升级是可以随时知道当前Pod部署的进度。

##### Horizontal Pod Autocaler(HPA)
Pod 横向自动扩容，通过追踪分析 RC 控制的所有目标 Pod 的负载变化情况，确定是否需要针对性地调整目标 Pod 的副本数。

##### Services
抽象服务出口。它就像一个基础版本的负载均衡器。

##### Volume
Pod 中能够被多个容器访问的共享目录，其生命周期与Pod相同跟容器无关。

#### Annotation
与 Lable 类似，也使用 key/value 键值对的形式定义，不同于 Lable 定义 Kubernetes 的元数据，它是用户任意定义的附加信息，以便于外部工具进行查找。
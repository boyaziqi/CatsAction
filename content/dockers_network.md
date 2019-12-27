title: Docker系列（三）
subtitle: 网络模式
date: 2017-12-10
category: Docker
tags: Docker

Docker的网络是可通过插件扩展的，默认已经存在五种
##### 内置默认网络模型
- bridge，默认网络模型，会在宿主主机创建一个虚拟网卡，多个容器的网络连接到上面。
- host，适用于单个独立运行的容器，把网络隔离取消，和宿主主机共用网络。
- overlay，可以让多个Docker Daemon之间网络互连，我觉得这需要分布式部署大型应用的时候很有用吧。
- macvlan，可以分配MAC地址给容器，看名字应该是类似交换机vlan机制的网络模型。
- none，对容器禁止所有网络模型。目的是为了使用自定义的网络驱动模型。

下面写写每个网络模型的机制及使用。

#### bridge
bridge是docker默认的网络模型。它会在宿主主机上创建一个虚拟网卡bridge0，所有容器连接到这个虚拟网卡，他们共享一个私有网段，并将网关设置为bridge0。
###### *创建一个bridge网络*
```bash
# 创建
docker network create my-net
# 查看
docker network ls
```
###### *链接一个容器到创建到网络*
```bash
docker create --name my-nginx \
  --network my-net \
  --publish 8080:80 \
  nginx:latest
```
###### *连接一个已经运行的容器到网络*
```bash
docker network connect my-net my-nginx
```
###### *断开容器和网络的链接*
```bash
docker network disconnect my-net my-nginx
```

#### overlay
后面再写这部分，目前没有环境测试多个Docker Daemon之间的通讯。查看官方文档[overlay](https://docs.docker.com/network/overlay/)

#### host
这种模式容器的网络和宿主机共享，未被隔离，因此没有自己的IP地址。因此，端口映射不生效 -p, --publish, -P, 和 --publish-all 被忽略。

#### vlan
可以工作在OSI网络模型的第二层和第三层。
```bash
# macvlan模式，工作在第二层
docker network create -d macvlan \
    --subnet=192.168.50.0/24 \
    --gateway=192.168.50.1 \
    -o parent=eth0.50 macvlan50
# ipvlan模式，工作在第三层
docker network create -d ipvlan \
    --subnet=192.168.210.0/24 \
    --subnet=192.168.212.0/24 \
    --gateway=192.168.210.254 \
    --gateway=192.168.212.254 \
     -o ipvlan_mode=l2 ipvlan210
```

##### Docker其他知识点
先记录下，后期抽空单个知识点深入写一篇文章。

- swarm

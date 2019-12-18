title: RabbitMQ系列第三篇
subtitle: 分布式部署
date: 2017-01-22
category: MQ
tags: RabbitMQ,Docker

#### 集群特点
RabbitMQ节点不完全拷贝。所以其他非所有者节点只知道队列的元数据，和指向该队列节点的指针。

![集群特点]({static}/images/rabbitmq-cluster-feature.png)

#### 集群节点类型
- 内存节点
- 磁盘节点

如果集群只有一个磁盘节点，当该节点宕机时，集群仍然运行，但是不能创建Queue，Exchange，Binding，
也不能增加用户，更改权限，集群节点删除和增加也不行。因此为了集群的健壮，应两个磁盘节点。

#### 基于Docker测试集群部署
待续

#### 镜像队列
待续

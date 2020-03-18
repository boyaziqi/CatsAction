title: MySQL高可用方案
date: 2018-09-30
category: MySQL
tags: MySQL, HA, Orchestrator, MGR

## 常见MySQL集群方案

##### 一，MHA高可用架构

###### *简介*

  MHA（Master High Availability）目前在MySQL高可用方面是一个相对成熟的解决方案，它由日本DeNA公司的youshimaton（现就职于Facebook公司）开发，是一套优秀的作为MySQL高可用性环境下故障切换和主从提升的高可用软件。


###### *优点*

- 方案成熟，基于MySQL现有的主从复制技术，配置不需要更改太多。

- 能做到在0~30秒之内自动完成数据库的故障切换操作，并最大程度上保证数据的一致性。

- 适用于大部分MySQL存储引擎。

###### *缺点*

- 依靠MySQL原生主从复制技术，而MySQL主从复制是异步同步的，理论上仍然会有数据丢失。

- 发生故障后排查问题，定位问题更加困难。

- 已经停止维护，存在对MySQL更高版本的兼容问题。

##### 二，Orchestrator高可用架构

###### *特点*

- 强大的可视化管理界面。

- 自身可以多节点部署，防止单节点问题。

- 支持跨数据中心管理。

##### 三，官方版MGR架构

MySQL5.7新增功能

##### 四，其他高可用架构

- MySQL NDB Cluster(官方) 

- MariaDB Galera Cluster

- Percona XtraDB Cluster(PXC)
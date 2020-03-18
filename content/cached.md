title: Redis随笔
date: 2017-03-02
category: Cached
tags: Redis, Memcached

## Redis主从复制的高可用解决方案
Redis-Sentinel是Redis官方推荐的高可用性(HA)解决方案，当用Redis做Master-slave的高可用方案时，如果master宕机，Redis自身并不能实现自动进行主备切换。

sentinel可以监控复制节点的状态，当主节点宕机后，它能根据选举方式选出后端的一个从节点作为新的master，sentinel还能监控多个master-slave集群，发现master宕机后能进行自动切换。

同时，sentinel本身也存在单点问题，通常sentinel也是一个集群。

## sentinel集群工作原理
- sentinel集群通过给定的配置文件发现master，启动时会监控master。通过向master发送info信息获得该服务器下面的所有从服务器。

- sentinel集群通过流言协议与其他sentinel通信，以此来发现监视同一个主服务器的其他sentinel；集群之间会互相创建命令连接用于通信。

- sentinel集群使用ping命令来检测实例的状态，如果在指定的时间内（down-after-milliseconds）没有回复或则返回错误的回复，sentinel会认为主节点宕机，但是并不会立即提升一个从节点为新的master，因为会存在误判的情况，此时为主观宕机。此时当sentinel集群中有一半以上的节点通告master为宕机状态时，此时为客观宕机，sentinel基于选举协议选举提升从节点为新的master，从节点之间根据优先级来决策谁会成为新的master，修复的节点重新上线后作为从节点工作。

更多Redis-sentinel，可以参考[运维那些破事](https://www.cnblogs.com/lizhaojun-ops/p/9447016.html)和我的[Redis Sentinel模式]({filename}/redis_sentinel.md)
title: 缓存知识点
date: 2019-10-13
category: Cached
tags: Redis, Memcached

记录Redis和Memcached学习和使用的问题及思考，先简单记录，再抽时间详细完善。 


##### 缓存可能存在的问题

###### 缓存雪崩
定义：缓存同时过期失效。    
解决方法：交错失效时间，或者限制访问后端db的并发量。

###### 缓存穿透
定义：缓存没有，数据库也没有。    
解决方法：可以通过布隆过滤器过滤恶意的请求key。或者缓存空值提高命中率。

###### 缓存击穿
定义：热点key未命中。    
解决方法：可以增加多级缓存解决。

##### Memcached和Redis的区别
- Memcached单进程多线程，而Redis单进程单线程。处理小数据时，Redis性能比Memcached高，而在100K以上的数据中，Memcached性能要高于Redis。
- Memcached只支持key-value数据类型，而Redis支持丰富的数据类型。
- Redis并不是将所有数据存储在内存中。当内存容量用完时，Redis会swap一部分数据到磁盘上，而且也支持数据持久化。
- 从内存利用率来讲，使用简单的key-value存储的话，Memcached的内存利用率更高。而如果Redis采用hash结构来做key-value存储，由于其组合式的压缩，其内存利用率会高于Memcached。
- Memcached本身并不支持分布式，因此只能在客户端通过像一致性哈希这样的分布式算法来实现Memcached的分布式存储。相较于Memcached只能采用客户端实现分布式存储，Redis更偏向于在服务器端构建分布式存储。
- Redis支持服务端的数据操作，而Memcached需要将数据拿到客户端修改再set回去，增加了io操作。

关于Memcached和redis对比，可以参考[Memcached和Redis区别](http://www.360doc.com/content/18/0309/11/11935121_735604822.shtml)

##### Redis主从复制的高可用解决方案
Redis-Sentinel是Redis官方推荐的高可用性(HA)解决方案，当用Redis做Master-slave的高可用方案时，如果master宕机，Redis自身并不能实现自动进行主备切换，sentinel可以监控复制节点的状态，当主节点宕机后，它能根据选举方式选出后端的一个从节点作为新的master，sentinel还能监控多个master-slave集群，发现master宕机后能进行自动切换。

同时，sentinel本身也存在单点问题，通常sentinel也是一个集群，因此，redis的复制集群通常是下面的结构

###### sentinel集群工作原理
- sentinel集群通过给定的配置文件发现master，启动时会监控master。通过向master发送info信息获得该服务器下面的所有从服务器。

- sentinel集群通过流言协议与其他sentinel通信，以此来发现监视同一个主服务器的其他sentinel；集群之间会互相创建命令连接用于通信。

- sentinel集群使用ping命令来检测实例的状态，如果在指定的时间内（down-after-milliseconds）没有回复或则返回错误的回复，sentinel会认为主节点宕机，但是并不会立即提升一个从节点为新的master，因为会存在误判的情况，此时为主观宕机。此时当sentinel集群中有一半以上的节点通告master为宕机状态时，此时为客观宕机，sentinel基于选举协议选举提升从节点为新的master，从节点之间根据优先级来决策谁会成为新的master，修复的节点重新上线后作为从节点工作。

更多Redis-sentinel，可以参考[运维那些破事](https://www.cnblogs.com/lizhaojun-ops/p/9447016.html)
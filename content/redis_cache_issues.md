title: 缓存问题及处理
date: 2017-01-22
category: Cache
tags: Redis,Memcached

## 前述
本篇收集Redis一些常见问题及解决方法，最后面是一些Redis资料链接。

## Memcached和Redis的区别
- Memcached单进程多线程，而Redis单进程单线程。处理小数据时，Redis性能比Memcached高，而在100K以上的数据中，Memcached性能要高于Redis。

- Memcached只支持key-value数据类型，而Redis支持丰富的数据类型。

- Redis并不是将所有数据存储在内存中。当内存容量用完时，Redis会swap一部分数据到磁盘上，而且也支持数据持久化。

- 从内存利用率来讲，使用简单的key-value存储的话，Memcached的内存利用率更高。而如果Redis采用hash结构来做key-value存储，由于其组合式的压缩，其内存利用率会高于Memcached。

- Memcached本身并不支持分布式，因此只能在客户端通过像一致性哈希这样的分布式算法来实现Memcached的分布式存储。相较于Memcached只能采用客户端实现分布式存储，Redis更偏向于在服务器端构建分布式存储。

- Redis支持服务端的数据操作，而Memcached需要将数据拿到客户端修改再set回去，增加了io操作。

关于Memcached和redis对比，可以参考：

[Memcached和Redis区别](http://www.360doc.com/content/18/0309/11/11935121_735604822.shtml)

## 缓存的一些问题
##### 1，缓存穿透

*定义:*

所谓缓存穿透，就是访问根本不存在的数据。当访问一个数据时，缓存不存在，则会直接查询数据库。数据库也不存在，就返回空。
如果有恶意用户访问大量不存在的数据，则会给数据库造成很大压力。

*解决方法:*

- BloomFilter。类似于hash表的算法。把所有可能的查询生成一个bitmap。每次请求数据时，都通过BloomFilter查看数据是否存在。
- 缓存空值，并设置一个较短的过期时间。这样同个不存在的数据查询请求反复出现时，就能命中缓存。

##### 2，缓存雪崩

*定义:*

缓存雪崩，就是缓存中大量数据同时失效。此时大量的数据请求就好转发到数据库，从而给数据库造成压力。

*解决方法:*

- 让失效时间不同。比如一定范围的随机时间，这样就避免了大量缓存同时失效。缺点是粒度不好把握。
- 可以限制并发量（比如利用锁和同步机制）。这样即使缓存大量失效，也不会有大量请求造成数据库压力。不过这种方法造成了服务性能的下降。

##### 缓存击穿

*定义:*

缓存击穿是缓存雪崩的特例。当某些热点数据失效时，它的请求会被发往数据库。在数据库请求并更新缓存的这段时间，如果有大量的热量请求，就会给数据库造成很大的压力。

*解决方法:*

- 增加二级缓存，不同的缓存设置不同的失效时间。这个解决方案也适用于缓存雪崩。
- 基于LRU的缓存换出策略。

---

## 后述

*一些资料：*

[Redis技术集](https://zhuanlan.zhihu.com/p/28073983)收集了一些Redis的技术讲解和使用场景按理。

[阿里云缓存架构](https://yq.aliyun.com/articles/290865)

[神奇的HyperLogLog算法](http://www.rainybowe.com/blog/2017/07/13/%E7%A5%9E%E5%A5%87%E7%9A%84HyperLogLog%E7%AE%97%E6%B3%95/index.html)

[Redis HyperLogLog结构](https://zhuanlan.zhihu.com/p/58358264)

[Redis Bitmap结构](https://segmentfault.com/a/1190000008188655)

[Redis Geo实战](https://www.jianshu.com/p/81bf3baa64e5)

[GeoHash讲解](https://zhuanlan.zhihu.com/p/35940647)

[GeoHash简单代码展示](https://github.com/GongDexing/Geohash)

[Redis命令参考](http://doc.redisfans.com/)
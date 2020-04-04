title: Redis系列二
subtitle: 内存淘汰机制
date: 2019-09-15
category: Redis
tags: Redis

## 前述
本篇先讲讲Redis过期key的删除机制，然后讲解Redis内存淘汰机制，最后针对LRU和LFU讲解和简单对比。

## 过期key删除策略

- 惰性删除：当读/写一个已经过期的key时，会触发惰性删除策略，直接删除掉这个过期key。

- 定期删除：每隔一段时间，Redis对数据库进行检查，删除里面的过期key。

##### 惰性删除

这种策略对CPU友好，但是可能导致内存浪费。如果一个已经过期的key永远不被访问，它所占用的内存也永远得不到释放。

##### 定期删除

定期删除默认每秒10次检查一次过期key，可以通过`hz`配置选项控制检查频率。定期删除会做下面检测和清除步骤。

1）随机测试100个设置了过期时间的key。

2） 删除所有发现的已过期的key。

3） 若删除的key超过25个则重复步骤1。

这是一个基于概率的简单算法，基本的假设是抽出的样本能够代表整个key空间，redis持续清理过期的数据直至将要过期的key的百分比降到了25%以下。这也意味着在任何给定的时刻已经过期但仍占据着内存空间的key的量最多为每秒的写操作量除以4。

## 内存淘汰机制

除了上面一小节的过期key删除策略，Redis还提供了内存淘汰机制。当使用内存超过`maxmemory`限定时，触发内存淘汰机制。Redis提供了以下几种内存淘汰机制。

- noeviction：当内存使用超出maxmemory限制时，客户端访问返回错误（大部分的写入命令，但是DEL命令例外）。

- allkeys-lru: 对所有的key应用LRU淘汰机制。

- volatile-lru: 仅对设置了过期时间的key应用LRU淘汰机制。

- allkeys-random: 随机回收所有的key。

- volatile-random: 随机回收设置了过期时间的key。

- volatile-ttl: 只对设置了过期时间的key进行回收，但优先回收存活时间（TTL）较短的key。 

## Redis LRU实现

Redis使用的是近似LRU算法，它跟常规的LRU算法还不太一样。

近似LRU算法通过随机采样法淘汰数据，每次随机取出一定数量的key，从里面淘汰掉最近最少使用的key。可以通过maxmemory-samples配置随机采样的key数量，值越大，越接近真实LRU算法。默认值为5。

Redis的近似LRU算法，避免了对所有的key操作，减少了内存消耗，避免了扫描所有key的时间复杂度。

## Redis LFU算法

LFU算法，全称Least Frequently Used。根据访问的频率淘汰访问相对不频繁的key。LFU避免了一个key很少被访问，而最近被访问一次而不被淘汰的问题。LRF算法是4.0新增的。

Redis LFU算法提供了下面两种策略：

- valatile-lfu：只对设置了过期时间的key应用LFU策略。

- allkey-lfu：对所有key基于LFU回收内存。

Redis4.0对LFU增加了两个配置。

```conf
lfu-log-factor 10
lfu-decay-time 1
```
> lfu-log-factor：可以调整计数器counter的增长速度，lfu-log-factor越大，counter增长的越慢。

> lfu-decay-time：是一个以分钟为单位的数值，可以调整counter的减少速度。

##### Redis LFU工作机制

Redis会为每个key对象维护一个计数器counter和最近一次计数被减少时的时间（总共24bit，LRU的最近访问时间拆分为两部分分，高位的16bit为最近计数器被减少时的时间，低位的8bit为计数器counter）。

当一个key被访问需要增加计数器counter时，需要根据两个因子r、p比较，当`r < p`时，counter自增1，否则不增加。其中r因子为`0-1`之间的随机数，p因子由当前的counter值和配置项`lfu-log-factor`共同决定。

需要减少counter值时，并不是总减少1。Redis会计算key对象最近一次被减少时间相对于目前时间过去了多少个lfu-decay-time，即`(now - last_dect_time) / lfu-decay-time`的值，counter即减去算出来的值。

> 基于现在时间和最近一次操作时间的差值，解决了
> 一个key一段时间访问频繁，从而counter值增加，但是后期访问频率比较低甚至不访问，如果只是简单的累加counter，那这种情况则不能很好的被清除。

下面的Redis源码展示了counter计数器增加和减少的逻辑，详细代码讲解可以参考本章最后面的参考资料链接**Redis中的LFU算法**。

```C
uint8_t LFULogIncr(uint8_t counter) {
    if (counter == 255) return 255;
    double r = (double)rand()/RAND_MAX;
    double baseval = counter - LFU_INIT_VAL;
    if (baseval < 0) baseval = 0;
    double p = 1.0/(baseval*server.lfu_log_factor+1);
    if (r < p) counter++;
    return counter;
}

unsigned long LFUDecrAndReturn(robj *o) {
    unsigned long ldt = o->lru >> 8;
    unsigned long counter = o->lru & 255;
    unsigned long num_periods = server.lfu_decay_time ? LFUTimeElapsed(ldt) / server.lfu_decay_time : 0;
    if (num_periods)
        counter = (num_periods > counter) ? 0 : counter - num_periods;
    return counter;
}
```

由于LFU需要根据counter排序，如果对所有的key操作，肯定会影响Redis的吞吐量。基于这个原因，可以参考LRU算法，给定一个固定的pool，随机选取一批key，再在被选中的key中应用LFU淘汰机制。

## 后述

*参考资料：*

*Redis官方文档：[Using Redis as an LRU cache](https://redis.io/topics/lru-cache)*

*[Redis的内存淘汰策略](https://juejin.im/post/5d674ac2e51d4557ca7fdd70)*

*[Redis中的LFU算法](https://www.cnblogs.com/linxiyue/p/10955533.html)*

*Redis系列其他文章：*

*[Redis Sentinel模式]({filename}/redis_sentinel.md)*

*[Redis概述和数据类型]({filename}/redis1.md)*
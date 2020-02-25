title: Redis Sentinel模式
date: 2020-01-09
category: Redis
tags: Redis

文章最后，我会基于Docker部署Redis主从和验证Sentinel模式。相关配置我已经放到我的GitHub，欢迎克隆交流学习。

##### Redis主从同步原理
###### 1，增量同步
主从服务器同步的是执行的指令流。当主服务器收到指令时，会将指令写到buffer（buffer大小固定，可配置更改），然后异步将执行指令同步到从服务器。
当buffer空间不足时，新收到指令会导致旧数据覆盖，这时会触发快照同步。

###### 2，快照同步
Redis主服务会生成快照文件dump.rdb，当从服务首次连接到主服务器上或主服务重启时，主服务将dump.rdb文件传送给从服务器，从服务清空旧数据，然后利用dump.rdb文件
恢复最新的数据，恢复完成后，再和主服务器行增量同步保持数据一致。

###### 3，主从同步流程
（1）从服务根据配置的ip和port连接到主服务，如何主服务设置口令需要提供相应口令。

（2）从服务和主服务成匹配后，先进行一次快照同步。

（3）快照同步完成后，主从服务进行增量同步。从服务会维护一个数据offset，并与主服务保持同步。

（4）主从服务会按一定频率给对方发送heartbeat，用了检测对方是不是正常在线。如果网络断开然后恢复，会自动重连，并通过offset判断是否需要快照同步。

（5）从服务不处理过期key。当某个key过期时，主服务会模拟一个DEL指令发送给从服务器。

<center>
![dockers_vm]({static}/images/redis_master_replication.jpg)
</center>

##### Sentinel模式简介
Redis主从服务采取读写分离，主服务负责写，从服务负责读。当主服务宕机时，Redis主从并不会从新选择主服务，这将导致整个主从服务无法正常工作。官方推荐的
主从同步高可用方案是Sentinel，它会监控和复制服务状态，当主服务宕机后，会根据选举算法从后端从服务选择新的主服务。Sentinel本身也有单点瓶颈的问题，因此也需要集群。

<center>
![dockers_vm]({static}/images/redis_sentinel.jpg)
</center>

##### 工作机制
Sentinel会运行三个定时任务（监控，通知，故障迁移）。当Redis主服务宕机后，会根据一定的机制选择一个领导Sentinel来执行故障迁移。主服务选择出来并配置成功后，领导Sentinel
通过slaveof ip port让其他从服务同步新的主服务。原来的主服务如果重新加入，才会成为新主服务的从服务。

###### 如何确认一个服务已经故障
当一个Sentinel ping不同一个服务节点时，并不会立即认为该服务节点故障（主观下线）。只有当所有Sentinel协商一致，才认为该服务节点故障（客观下线）。

###### 领导选举机制
- 每个做主观下线的Sentinel将向其它Sentinel发送命令，要求将自己设为领导Sentinel。
- 收到命令的Sentinel如果没有同意过其它Sentinel的领导请求命令，那就同意，否则拒绝。
- 如果该Sentinel发现自己票数超过Sentinel集合的一半且达到quorum，该Sentinel将成为领导Sentinel。
- 如果此过程有多个Sentinel成为领导Sentinel，那么将等待一段时间重新进行选举。

###### 从服务节点选择机制
- 选择slave-priority（slave优先级）最高的slave节点，如果有返回，没有继续。
- 选择复制偏移量最大的slave节点（复制最完整），如果有返回，没有继续。
- 选择runId最小的slave节点。

##### 测试
为了方便验证和部署Redis主从，我基于Docker-compose构建了验证环境，相关信息查看文章开头。docker-compose.yml文件内容如下。
```yaml
version: '3'
services:
    redisA:
        image: redis
        restart: always
        ports:
            - "6376:6379"
        volumes:
            - ./config/redis1/:/usr/local/etc/redis/
            - ./logs/redis1/:/var/log/redis/
        command: redis-server /usr/local/etc/redis/redis.conf
    redisB:
        image: redis
        restart: always
        ports:
            - "6377:6379"
        volumes:
            - ./config/redis2/:/usr/local/etc/redis/
            - ./logs/redis2/:/var/log/redis/
        command: redis-server /usr/local/etc/redis/redis.conf
    redisC:
        image: redis
        restart: always
        ports:
            - "6378:6379"
        volumes:
            - ./config/redis3/:/usr/local/etc/redis/
            - ./logs/redis3/:/var/log/redis/
        command: redis-server /usr/local/etc/redis/redis.conf
```
在终端执行`docker-compose up`开启三个Docker容器，并挂载配置和日志相关的目录。其中RedisA作为主服务节点，RedisB和RedisC作为从服务节点。在从服务节点配置文件redis.conf上指定主服务节点。
```bash
slaveof redis-replication_redisA_1 6379
```
通过上面的配置，一个简单的一主两从的Redis主从服务就搭建好了，可以在主服务节点set一个key严重从服务节点是否正常复制。
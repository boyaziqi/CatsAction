title: 面试知识点回答整理2
subtitle: 分布式部署
date: 2017-01-22
status: draft
category: interview
tags: hash,cache

#### Python CI知识
工具有Jenkins，buildbot，Travis，Tox。我们选择了Buildbot，是因为它是Python开发的，而且开源。
Travis CI对闭源软件不免费。后续写一篇利用buildbot+tox实现自动化测试及CI的文章。

#### Python 测试包
pytest，unitest，mock, nose, doctest, tox

#### Python2和Python3的区别
- string编码。Python3默认是Unicode，Python2是ASCII。
- Python没有xrange，只有range。
- 字典keys，views，iterms返回迭代器。
- Python3类都是新式类。
- 标准库有变化。

#### Redis持久化
有两种方式：快照（RDB文件）和追加写记录（AOF文件）

#### protobuf知识
- 类型：message，service
- 数据类型：string，int，enum，float，bool，byte。
- 修饰符：required，optional，repeated。

#### IO模型
select，poll，epoll

#### Restful风格
- 系统上的一切对象都要抽象为资源；
- 每个资源对应唯一的资源标识（URI）；
- 对资源的操作不能改变资源标识（URI）本身；
- 所有的操作都是无状态的等等。

#### 短连接的实现方式（腾讯面试题）

#### session机制及实现方法
好的

#### Django设计思想
观察者模式，也叫发布订阅模式。Django的信号就是。

#### 选择Django的原因
- 功能完善，要素齐全。自带模板引擎和管理后台。
- 对数据库支持全面和完善的ORM。
- 自带缓存模块。
- 完善的用户认证和可扩展。
- 灵活的Middleware。
- 文档齐全，社区生态好。

#### 如何测试数据库
创建一个临时数据库表，测试完成后删除。

#### 针对数据中心重构了哪些代码
- 增加了一张缓存表。
- 封装了一些共用SDK，如上游调用的一些工具, 共同的结算。
- 拆分代码为几大功能模块。

#### 微服务之间如何通信
- RPC
- 进程间通信（消息队列）
- HTTP

#### Python协成实现机制及AsyncIO库

#### 为什么选择了RPC及gRPC？
- 对输入和输出校验，集成了认证
- 写起来清晰，像调用本地的方法。
- 开发即文档，不需要再写单独的文档接口。

#### 选择gRPC而不是Thrift的理由
gRPC文档更完善，而且Protobuf语法友好。

#### 项目中遇到的困难、挑战和解决方法
- 统计数据库的问题
- too many open file（ulimit -n 65535调整最大文件限制数）。官方bug，线程池创建回收竞态。
- 服务拆分问题及服务发现
- MySQL主从复制server_id未生效（配置应放到[mysqld]模块下）
- 订单定时取消的问题
- 定时发送短信通知的问题
- 取消和支付并发了，取消了另一方支付了（怎么解决）
- 购物车（可以基于Redis解决）
- 查找Ip、电话归属（Redis解决方案）
- 地区排序（可以基于Redis解决）
- 医生排序（可以基于Redis解决）
- Redis缓存统计页面访问信息
- 找到一个Redis事务（multi, watch）应用场景
- 统计中消息队列的应用
- 记录最近查询
- 怎么样实现全文搜索（知乎，GitHub那样过滤任何部分）
- 怎么解决32位信号量计数器溢出问题
- redis实现延迟发布活动，或延迟上架
- 反向索引
- 关注者列表
- Nginx代理和缓存机制
- Zookpeer队列
- 缓存中的CAP问题
- 线程共享数据问题
- 分布式事务
- zookpeeper
- 短链接的实现（如何基于Redis）
- 抢空包

#### 想找一份什么样的工作
- 云平台开发的工作
- 底层的开发，而不是纯面向业务
- 在线教育、商城、视频网站

#### 孤儿进程和僵尸进程
###### 孤儿进程
父进程退出，但是子进程还在运行，子进程就成年孤儿进程。孤儿进程会被1号进程收养（init进程)

###### 僵尸进程
一个进程使用fork创建子进程，如果子进程退出，而父进程并没有调用wait或waitpid获取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中。这种进程称之为僵死进程。

###### 僵尸进程解决方法
	杀死父进程，让僵尸进程被1号进程托管，然后被回收。

#### DDos攻击解决方案
资源隔离，防止ip泄露，中间件

#### B+树为什么适合做索引
- 只有叶子节点存储指向记录的指针，降低了高度，而且可以容纳更多叶子节点。
-  叶子节点之间通过指针来连接，范围扫描将十分简单，而对于B树来说，则需要在叶子节点和内部节点不停的往返移动。

#### Django如何配置多数据库支持
略

#### TCP控制时间的头部
选项（4bit）中kind=8是可以填充时间戳。

#### 性能测试工具
- ab
- http_load

#### MySQL数据库性能测试工具
- mysqlslap（自带）
- MySQL Benchmark Suit
- Super Smark
- Database Test Suit
- sysbench
- MySQL BENCHMARK函数

#### MySQL服务器性能分析（响应时间）
1. Percona Toolkit的pt-query-digest命令分析慢查询日志，定位到导致慢查询的单条语句；
2.用`show profiles`详细分析单条语句的执行时间。

#### 如何排除MySQL查询慢是慢查询语句问题还是服务器整体问题
- 使用`show global status`命令查看thread_runing，queries等字段的情况，很大表明服务器等待任务过多导致响应时间变慢；
- 使用`show processlist`命令查看查询状态；
- 使用慢查询日志。

#### Dcoker内存和CPU限制
- -m --memory限制内存
- -cpu-shares 512限制权重，默认是1024
- --blkio-weight 600限制io权重，默认是500

#### MySQL主从复制原理

mysql主从是异步复制过程

master开启bin-log功能，日志文件用于记录数据库的读写增删
需要开启3个线程，master IO线程，slave开启 IO线程 SQL线程，
Slave 通过IO线程连接master，并且请求某个bin-log，position之后的内容。
MASTER服务器收到slave IO线程发来的日志请求信息，io线程去将bin-log内容，position返回给slave IO线程。
slave服务器收到bin-log日志内容，将bin-log日志内容写入relay-log中继日志，创建一个master.info的文件，该文件记录了master ip 用户名 密码 master bin-log名称，bin-log position。
slave端开启SQL线程，实时监控relay-log日志内容是否有更新，解析文件中的SQL语句，在slave数据库中去执行。

#### MySQL主从复制遇到的问题

###### 1.server—id配置没生效
放错位置，应该放到[mysqld]模块

###### 2. start slave启动主从报uuid相同错误
数据目录下的auto.cnf里的server-uuid配置相同（为什么相同，不是自己生成的吗）。    
答案：我用的Docker安装MySQL，两个数据目录当时直接拷贝的，导致一样。

###### 3. 启动slave时报错Slave failed to initialize relay log info structure from the repository

这是因为slave的slave_relay_log_info表存储的还是比较旧的信息，需要情况。用下面两个命令对比数据是不是不一致。
```bash
mysql>select * from mysql.slave_master_info \G;
mysql>select * from mysql.slave_relay_log_info\G;
```
其中Master_log_name和Master_log_pos需要一致，不一致清空再开启主从。用下面命令清空。
```bash
mysql>reset slave;
```
下面的命令开启主从复制，读写分离。
```bash
mysql>start slave;
```
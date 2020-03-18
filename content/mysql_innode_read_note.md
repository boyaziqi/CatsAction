title: 《MySQL技术内幕:InnoDB存储引擎》读书笔记
date: 2018-10-10
category: 读书笔记
tags: DB,SQL,MySQL

## 第一章：MySQL体系结构和存储引擎
##### 1，MySQL组成
- 连接池组件
- 管理服务和工具组件
- SQL接口组件
- 查询分析组件
- 优化器组件
- 缓冲组件
- 插件式存储引擎
- 存储文件

##### 2，MySQL存储引擎
- InnoDB
- MyISAM
- NDB
- Memory
- Archive
- Federated
- Maria

## 第二章：InnoDB存储引擎
##### 1，InnoDB体系结构

1），后台线程

默认情况下，InnoDB有七个后台线程。1个master thread，4个IO thread，1个锁线程，1个监控线程。

4个IO thread分别是insert buffer thread，log thread，read thread，write thread。

2），内存

InnoDB存储引擎内存由以下几部分组成

- 缓冲池（buffer pool）
- 重做日志缓冲池（redo log pool）
- 额外内存吃（additional memory pool）

buffer pool：

buffer pool占内存最大块，用来存放各种数据的缓存（按每页16K操作）。

buffer pool数据页类型有如下几种，其中data page和index page占很大一部分。

- data page（数据页）
- index page（索引页）
- insert buffer（插入缓冲）
- adaptive hash index（自适应哈希索引）
- lock info（InnoDB存储的锁信息）
- data dictionary（数据字典信息）

##### 2，master thread

InnoDB主要工作由master thread完成，master thread有以下几个loop（循环）组成。master thread会根据数据库运行
情况在几个循环之间切换。

- main loop（主循环）
- background loop（后台循环）
- flush loop（刷新循环）
- suspend loop（暂停循环）

master thread潜在问题：

InnoDB对IO有限制，在硬盘性能飞速发展的今天，不能很好的利用硬盘性能。最新的版本中增加了几个对master thread的可配置参数。

##### 3，关键特性

- 插入缓冲（针对非聚集索引插入的优化）
- 两次写
- 自适应哈希索引

## 第三章：文件
##### 1，表结构定义文件

MySQL自身的文件，以frm后缀结尾，每个表都拥有单独的表结构定义文件。

##### 2，InnoDB存储引擎文件

1），表空间文件

可以所有表放到一个表空间文件里，也可以通过参数配置一个表一个表空间文件。默认的表空间文件是多个表共用的ibdata1文件。

2），重做日志文件

- ib_logfile0
- ib_logfile1

## 第四章：表
InnoDB的表是索引组织的，聚簇索引的叶子节点存储的即为行记录（数据）。

##### 1，InnoDB逻辑存储结构

从InnoDB逻辑上看，所有数据都被存储在一个空间中（表空间）。表空间由以下几部分组成，其中上面的层包含下面层。

- 段（segment）
- 区（extent），默认大小为1M，即64页。
- 页（page），默认每页大小为16k。
- 行（row）

##### 2，InnoDB行记录格式

- Compact（默认）
- Redundant（为兼容之前版本保留）

1），Compact格式

| 变长字段长度列表 | NULL标志位 | 记录头信息 | 列1数据 | 列2数据 | ...... |

2)，Redundant格式

| 字段长度偏移列表 | 记录台信息 | 列1数据 | 列2数据 | ...... |

##### 3，InnoDB数据页结构

- File Header（文件头）
- Page Header（页头）
- Infimun和Supremum Records
- User Records
- Free Space
- Page Directory
- File Trailer

##### 4，分区表
分区功能不是在存储引擎功能完成的。MySQL支持水平分区（按行分区），而不支持垂直分区（按列分区）。
MySQL支持的分区为局部分区（一个分区即存放了数据，又存放了索引），而不支持全局分区（数据存放在各个分区中，但索引全部存放在一个对象中）。

MySQL数据库支持以下几种类型的分区：

- Range分区：根据分区列连续区间分区。
- List分区：相对于Range分区，List分区是离散的。
- Hash分区：根据用户自定义表达式的返回值来分区。
- Key分区：根据MySQL数据库提供的哈希函数来分区。

## 第五章：索引和算法

##### 1，InnoDB支持的索引类型

- B+树索引
- Hash索引
- 全文索引

关于B树和B+树的详细讲解，可以查看[B+树](https://www.cnblogs.com/nullzx/p/8729425.html)

##### 2，B+树索引类型

1），聚集索引

叶子节点存储了整行的记录数据。通常一个表的聚簇索引就是主键索引。一个表只能有一个聚簇索引。

2），辅助索引（普通索引）

叶子节点存储键和行记录的主键，因此查询数据可能产生回表，可以通过索引覆盖解决。

关于聚簇索引和索引覆盖，查看我的另一篇博客[聚簇索引]({filename}/mysql3.md)

3）索引管理

- 创建索引：create index
- 删除索引： drop index
- 查看索引信息： show index from table

4）一些索引信息

- 联合索引
- 索引覆盖
- 优化器（未索引覆盖的情况下，优化器可能选择走聚簇索引）


## 第六章：锁

锁是数据库区别于文件系统的一个关键特性。锁用于管理共享资源的并发访问。不同的数据库和存储引擎有不同的锁实现机制。

##### 1，锁的类型
- 共享锁
- 排它锁

##### 2，锁的机制

##### 3，锁的算法
- Record Lock：单个行记录上锁
- Gap Lock：间隙锁，锁定一个范围，但不包括行记录本身
- Next-Key Lock：上两种锁的结合

##### 4，锁问题
- 脏读：可以读取到脏数据（一个事物可以读取到另一个事务未提交的数据）
- 丢失更新：一个事务在另一个事务在读取的过程中做了修改，导致两次读取的数据集不一致
- 不可重复度：一个事务的更新操作会被另一个事务的更新操作所覆盖（数据库锁并不会有这个问题，但是用户层面可能产生这个问题）

##### 5，死锁
死锁是两个以上的事务在执行过程中，因争夺资源而造成互相等待的现象。

解决方法：

- 超时回滚重做
- wait-for Graph（等待图）

## 第七章：事务
##### 1，事务特性
- 原子性（atomicity)
- 一致性（consistency）
- 隔离性（isolation）
- 持久性（durability）

##### 2，事务隔离级别
- READ UNCOMMITTED
- READ COMMITTED
- REPEATABLE READ
- SERIALIZABLE

##### 3，分布式锁
分布式事务指的是允许多个独立的事务资源参与到一个全局的事务中。全局事务要求在其中的所有参与的事务，要么都提交，要么都回滚。分布式事务允许不同数据库之间的分布式事务，常见于银行系统的转账业务。

## 第八章：备份与恢复
- 热备
- 冷备
- 温呗

##### 1，冷备
对于InnoDB，需要备份表结构frm文件，共享表空间文件，独立表空间文件.ibd，重做日志。

##### 2，热备
- ibbackup
- XtraBackup

##### 3，快照备份
MySQL本身不支持快照备份，但是可以基于操作系统实现。比如Linux的LVM对数据文件进行管理。

##### 4，逻辑备份
- mysqldump
- SELECT INTO...OUTFILE

##### 5，主从复制
主从复制是MySQL的一种高可用解决方案，主要有如下三个步骤。

1. master节点将数据更改记录到bin-log日志中。
2. slave节点把主服务的bin-log日志复制到自己relay-log日志里。
3. slave节点从做relay-log日志，把数据更改更新到自己的数据库上，以到达数据和master节点最终一致。


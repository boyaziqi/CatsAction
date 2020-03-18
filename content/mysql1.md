title: MySQL系列一
subtitle: 体系结构和存储引擎
date: 2019-08-04
category: MySQL
tags: DB,SQL,MySQL

MySQL知识点很多，有人专门整理了[MySQL学习的书籍](http://mingxinglai.com/cn/2015/12/material-of-mysql/)

#### 体系结构
MySQL被设计成单进程多线程的数据库。

![MyzSQL体系结构]({static}/images/mysql_architecture.png)

如上图，MySQL系统结构由八部分组成。

- 连接池组件
- 管理服务和工具组件
- SQL接口组件
- 查询分析组件
- 优化器组件
- 缓冲组件
- 插件式存储引擎
- 存储文件

#### 名词解释
OLTP：联机事务处理  
OLAP：联机分析处理   
页： InnoDB存储引擎的表空间由段（segment），区（extent）和页（page）组成，一页默认16K。  
聚集索引：正文内容按照一个特定维度排序存储，这个特定的维度就是聚集索引。比如InnoDB存储引擎里的id主键。  
非聚集索引：非聚集索引项顺序存储，但索引项对应的内容却是随机存储的；如自定义的普通索引。

#### 存储引擎
MySQL存储引擎是插件式的，可以根据MySQL预定义的接口开发自己的存储引擎。MySQL的存储引擎是表维度的，而不是数据库维度。同一个库不同表可以有不一致的存储引擎。
###### *InnoDB*
InnoDB主要用于OLTP，行锁设计，支持事务和外键，支持非锁定读。  
InnoDB将数据存储在一个逻辑表空间，可以配置指定每张表存放在单独的ibd文件中。支持裸设备来建立表空间。 
InnoDB通过多版本并发控制（MVCC）实现非锁定度及支持高并发。支持事务的四种隔离级别（READ UNCOMMITTED，READ COMMITTED，REPEATABLE READ，SERIALIZABLE）  
InnoDB提供了插入缓冲，二次写，自适应哈希索引，预读等高性能和高可用功能。   
InnoDB数据采用聚集的存储方式，每张表的数据按照主键的顺序存放。这种存数据方式有回表的现象。可以通过建立适当的聚合索引包含需要查询的字段规避。
###### *MyISAM*
不支持事务和外键，表锁。支持全文索引。对于OLAP应用速度很快。   
MyISAM存储引擎表有MYD和MYI组成。MYD存放数据，MYI存放索引。
###### *NDB*
NDB存储引擎是一个集群存储引擎。数据存在内存。页面锁，但也支持表锁。   
NDB存储引擎的连接查表操作是在数据库实例层面完成的，而不是引擎层面。因此复查的连表查询网络开销比较大，可能导致性能降低。
###### *Memory*
Memory存储引擎数据存放内存，使用哈希索引。只支持表锁，不支持TEXT和BLOG类型。VARCHAR类型按CHAR类型存储，造成空间浪费。
###### *Archive*
Archive存储引擎只支持SELECT和INSERT操作，使用压缩算法压缩数据行。支持行锁，但并不支持事务安全。主要用于高速的插入和压缩功能。

#### MySQL连接方式
- TCP套接字
- 命名管道
- 共享内存
- Unix域套接字

MySQL知识点很多，先简单记录上面的知识点。后期把开篇提到的MySQL相关书籍读完，再抽时间更新和完善MySQL知识点内容。

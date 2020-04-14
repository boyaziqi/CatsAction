title: 面试知识点回答整理
subtitle: 分布式部署
date: 2017-01-22
status: draft
category: interview
tags: hash,cache

#### 一致性哈希
一致性Hash算法将整个哈希值空间组织成一个虚拟的圆环，如假设某哈希函数H的值空间为0-2^32-1。首先将服务器hash（通过ip或主机名)
映射到Hash环上。定位数据资源的时候，将数据key用相同的hash方法算出hash值，并找到key在hash环上的位置。顺时针查找，遇到的第一台服务器即为
数据定位的服务器。一致性hash有很好的扩展性和容错性，即增加和减少一台服务器时，影响的只是对应区段的数据映射。不过一致性hash也会造成数据倾斜（数据节点太少且分布不均）。
可以通过增加虚拟节点和将环映射到均匀的线上。

#### IO复用
IO复用也是一种阻塞式调用，不过它阻塞于多个描述符，即可以同时等待多个描述符就位。只要其中之一满足条件，调用就返回。<br>
常见的IO复用类型有select，poll和epoll。
###### *区别*
- select和epoll最大连接数限制为1024（32位）和2048（64位）。
- select和epoll采用轮询方式查看就绪的sockets。
- epoll内存拷贝次数少。select和poll每次都需要将用户态拷贝到内核空间，epoll却只需要一次。

#### 阻塞，非阻塞，异步，同步

#### 360电话面试问题

#### HTTP常用头
###### *Request Headers*
- Accept：text/html
- Accept-encoding: gzip
- Accept-Language: en-US
- Cache-control: max-age=0
- Cookie
- Refer：https://www.baidu.com/xxxxxxxxxx
- User-agent：Mozilla/5.0 

###### *Resonse Headers*
- Accpet-ranges：bytes
- Content-length：24211
- Content-type：text/html
- Content-encoding：br
- Age：1037016
- Date：Thu, 15 Feb 2018 20:31:45 GMT
- Expires：Fri, 01 Feb 2019 17:33:57 GMT
- Last-modified：Mon, 12 Dec 2016 14:45:00 GMT
- Vary：Accept-Encoding
- Server: gws
- Set-cookie:
- X-frame-options: SAMEORIGIN
- X-xss-protection：1; mode=block
- Etag：

#### CSRF
CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。
你这可以这么理解CSRF攻击：攻击者盗用了你的身份，以你的名义发送恶意请求。下面是防止方法。
- 生成一个随机数
- 每次请求时要求输入验证码 

#### XSS

#### 进程，线程，协成

#### Docker entry CMD区别
见[对比](https://zhuanlan.zhihu.com/p/30555962)

#### MySQL回表
参考[InnoDB聚集索引普通索引，回表，索引覆盖](https://www.cnblogs.com/myseries/p/11265849.html)

#### MySQL存储引擎
#### MySQL索引
MySQL索引类型：普通索引，唯一索引，主键索引（表只能有一个索引，必须唯一，不能允许空值），组合索引，全文索引（旧版本只有MyISAM支持，新版本InnoDB也支持）<br>
全文索引：普通索引通过数值的精确比较确认搜索范围，而全文索引通过模糊匹配确认查询。常用于char，text类型字段上。<br>
suo
#### MySQL事务
#### MySQL锁
#### MySQL优化的一些理解

#### Python垃圾回收机制
引用计数，标记清除，分代回收

#### Python CI/CD工具
可以使用最流行的jenkins，还有自带的BuildBot，Tox。博派通达使用Buildbot构建代码，是用Tox自动化执行测试。

#### Python自动运维工具
SaltStack，Supervisor，Ansible

#### Linux Find命令
参考https://www.cnblogs.com/RXDXB/p/11696751.html
1, 基本用法

```bash
find /home -name test
find /home -name "*.py"
```

2, 指定查找类型

```bash
# 通过-type指定，d目录，f文件
# 在/home目录下查找test目录
find /home -type d -name test
```
3, 根据权限查找
```bash
find /home -type f -perm 0777 -print
find /home -type f -perm /u=r
```
4, 查找空文件
```bash
find /home -type f -empty
```
5, 根据用户和组来查找
```bash
find /home -user root -name test
find /home -group mysql -name test
```

6, 根据文件创建，修改，访问时间查找

```bash
# -mtime   -n +n                 #按文件更改时间来查找文件，-n指n天以内，+n指n天以前
# -atime    -n +n                 #按文件访问时间来查GIN: 0px">
# -ctime    -n +n                 #按文件创建时间来查找文件，-n指n天以内，+n指n天以前
find . -ctime -20
```

7, 根据文件尺寸查找（-size)

#### 两台Linux主机拷贝文件的方式
scp，ftp，rsync

#### Linux查用命令汇总
- ps
- cp（-p保留权限拷贝）
- 查看端口的命令：netstat，lsof(lsof -i :8088)
- 查看负载（w，uptime，iostat。可以显示1m，5m，10m平均负载值）
- 查看cpu: cat /proc/cpuinfo
- 查看磁盘信息：fdisk -l
- 查看内存信息： cat /proc/meminfo， free
- 查看硬盘目录占用空间大小：du -h /home
- 磁盘分区：fdisk
- 磁盘挂载：mount
- 抓包命令：tcpdump
- io监控命令： iotop， iostat。
- 网络速率测试（Python工具speedtest）
- ip相关命令(ifconfig，hostname，ip addr show)
- 开机自启动（systemctl enable httpd。conetos6用systemd。也可以给~/.bashrc加启动脚本，或者放到/etc/rc.local添加启动脚本）
- 服务管理命令：systemctl。

#### systemctl服务类型
- Service unit：系统服务
- Target unit：多个 Unit 构成的一个组
- Device Unit：硬件设备
- Mount Unit：文件系统的挂载点
- Automount Unit：自动挂载点
- Path Unit：文件或路径
- Scope Unit：不是由 Systemd 启动的外部进程
- Slice Unit：进程组
- Snapshot Unit：Systemd 快照，可以切回某个快照
- Socket Unit：进程间通信的 socket
- Swap Unit：swap 文件
- Timer Unit：定时器
```bash
systemctl list-units
systemctl status
sudo systemctl stop apache.service
systemctl list-unit-files --type=target
```

#### 常见设计模式
- 单例模式：Python可以通过装饰器，元类，或者类属性实现
- 策略模式
- 代理模式
- 观察者模式，又叫订阅发布模式，生产者消费模式。
- 装饰器模式
- 迭代器模式
- 适配器模式
- 工厂模式
- 命令模式
- 组合模式
- 模板方法模式
- 访问者模式

#### Python 异步编程
进程，线程，协成
asyncio：get_event_loop， run_until_complete， get_running_loop

#### 常用的Python标准库
- re
- string
- datetime
- time
- weakref
- math
- enum
- random
- collection(OrderDict, DefaultDict, ChainMap, Counter)
- collection.abc
- decimal
- itertools(chain)
- functiontools
- pickle
- os
- logging
- threading
- asyncio
- urllib
- unittest
- unittest.mock
- sys
- types
- hashlib

#### 明源云笔试题
- 写出几个Python优雅的写法。
- *args和**kwargs含义及作用。
- tuple,list, dict, set区别。
- Python多线程和多进程的区别。
- 二分查找
- 生产者消费者实现
- 经典的找出部门最高工资sql
- 微服务优缺点
- 进程间通信方式
- 一个Python代码输出题
- solid原则
- 协程不适合什么场景。
- 如何优化单机Gunicore/sWsgi性能。

#### 明源云一面
- 技术选型的出发点（简历）
- 代码规范的一些思想（简历）
- Python垃圾回收机制，面试官让深入谈谈标记清零
- MySQL索引常见索引数据结构（我回答Hash索引和BTree+索引）
- 接上一问，详情谈谈Hash索引和BTree+索引的区别及应用场景。
- 主键索引和普通索引的区别（需要谈查询机制的区别）。
- 唯一索引和普通索引的区别（需要谈查询机制的区别）。
- 聊Docker，问有没有K8S经验（我答没有实际项目中的经验)
- Docker怎么限制CPU、内存、IO等资源。
- 接上一问，Docker限制资源的底层原理。
- 如果拷贝Docker里的文件到宿主机（我抖了一个机灵，回答挂载数据卷就可以写到本机。然后回答还可以通过网络拷贝如scp。但是面试官想要的没有启动的一个容器呢，我一时想不起。在面试官引导下，我明白了，UnionFS挂载的就是本地资源，找到挂载点就可以拷贝了。面试官人真好）
- 聊了一些怎么学技术，在看哪些书。
- 问我想找一份什么样的工作。
- 有什么想问的（我问了团队成员情况，文化氛围，资源权限等）

#### 量城
0，Redis单线程为啥还这么高效。

答：单线程，避免了线程切换开销；内存操作，没有太多IO开销；多路复用机制。

0.1，Python装饰器原理（回答闭包），那简单谈谈闭包的原理。

1，基于Redis实现关注者列表，要求可以根据关注者时间排序，然后可以找出共同关注的人以及哪些人关注我。

哪些人关注了我，我回答的是再用一个zset，但看面试官表情感觉不满意，是否可以基于好友的关注列表实现。

2，MySQL Join、Left Join、Right Join的区别。

3，MySQL倒排索引。

4，为什么选择用gRCP。（我简单回答了下HTTP2的特点）

5，查找一个单项链表的倒数第K个数，要求只能遍历一遍，空间复杂度不增加。

思路：用两个指针，当两个指针刚好相隔k-1位置时，第一个指针刚好指向第K个位置的数。（LeetCode题目https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/）

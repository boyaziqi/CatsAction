title: MySQL系列四
subtitle: 分区表
date: 2019-08-14
category: MySQL
tags: 数据库, 数据结构, MySQL

## 前述
分区表对用户来说仍然是一个独立的逻辑表，但是底层由多个物理子表组成。首先我们使用下面的语句创建一个分区表，来看看分区表的组成。对于分区表的创建类型，后面会讲。

```mysql
CREATE TABLE user_partition(
    id INT,
    name char(20),
    age int
) 
PARTITION BY RANGE (age) (
    PARTITION u1 VALUES LESS THAN (6),
    PARTITION u2 VALUES LESS THAN (18),
    PARTITION u3 VALUES LESS THAN (30),
    PARTITION u4 VALUES LESS THAN (50),
    PARTITION u5 VALUES LESS THAN (65),
    PARTITION u6 VALUES LESS THAN (80),
    PARTITION u7 VALUES LESS THAN (100),
    PARTITION uother VALUES LESS THAN (MAXVALUE) 
);
```
我在测试库`partition_db`创建了一个分区表`user_partition`，并根据年龄范围存储在8个子分区表中。用`show tables`看看建表情况，显示的情况和普通表一样，只有一个。这也说明了分区表对用户逻辑上只有一个。

```bash
mysql> show tables;
+------------------------+
| Tables_in_partition_db |
+------------------------+
| my_range_datetime      |
| user_partition         |
+------------------------+
2 rows in set (0.01 sec)
```

接下来我们看看底层存储情况，进入MySQL数据存储目录，在Linux系统上，默认是/var/lib/mysql，具体位置要根据你的配置。找到`partition_db`库目录，通过`ls -l | grep user`查看表文件情况。

```bash
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u1.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u2.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u3.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u4.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u5.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u6.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#u7.ibd
-rw-rw----  1 xufan  staff  98304  3 19 19:43 user_partition#P#uother.ibd
-rw-rw----  1 xufan  staff   8614  3 19 19:43 user_partition.frm
-rw-rw----  1 xufan  staff     52  3 19 19:43 user_partition.par
```
上面是我的机器上显示结果。可以看到，分区表底层存储对应的是多个分区子表，这里是8个，就是上面展示的以#分隔命名的标文件。`user_partition.frm`文件存储表结构，`user_partition.par`存储分区信息。

由于分区表是对底层表的封装，所以索引等也是独立建立在分区表子表上，而没有全局索引。对分区表的请求，都会通过句柄对象，转换为对存储引擎接口的调用，最后落实到具体的分区子表上。

## 分区表的操作

##### 1: 查看分区
```mysql
mysql> SELECT PARTITION_NAME,TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'user_partition';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| u1             |          0 |
| u2             |          0 |
| u3             |          0 |
| u4             |          0 |
| u5             |          0 |
| u6             |          0 |
| u7             |          0 |
| uother         |          0 |
+----------------+------------+
8 rows in set (0.01 sec)
```
我们看到，`user_partition`分区表有8个分区子表组成。

##### 2: 增加和删除分区子表

```mysql
ALTER TABLE user_partition ADD PARTITION (PARTITION u6_1 VALUES LESS THAN (90));
```
执行上面的命令，会报错`MAXVALUE can only be used in last partition definition`。可以看到，增加分区只能递增的形式，新分区不能再包含已有分区的值。

用下面的命令先删除最后一个分区

```mysql
ALTER TABLE `user_partition` DROP PARTITION uother;
```

再执行上面的命令，现在报`VALUES LESS THAN value must be strictly increasing for each partitio`，这是因为上面所说的，新增加的子分区不能包含已有分区的值。

将增加分区的数值改改，如下，执行成功。

```mysql
ALTER TABLE user_partition ADD PARTITION (PARTITION u6_1 VALUES LESS THAN (120));
```

##### 3: 分区表的使用

分区表的使用和普通表一样，直接插入就行，查询也是。

```mysql
INSERT INTO user_partion(name,age) VALUES("zhangsan", 30);
INSERT INTO user_partion(name,age) VALUES("wanger", 105);
```
```mysql
mysql> select * from user_partition;
+------+----------+------+
| id   | name     | age  |
+------+----------+------+
| NULL | zhangsan |   30 |
| NULL | wanger   |  105 |
+------+----------+------+
2 rows in set (0.00 sec)
```

对应到底层，会先锁住分区表的所有底层表，再调用存储引擎接口操作对应的底层表。

## 分区表的创建类型

##### 1: RANGE分区

基于属于一个给定连续区间的列值，把多行分配给分区。基于分区的列判断数值需是整型，如果不是需要用函数转换。如时间类型，可以用to_days函数转换为整型。

##### 2: LIST分区

LIST分区和RANGE分区类似，区别在于LIST是枚举值列表的集合，RANGE是连续的区间值的集合。二者在语法方面非常的相似。

##### 3: HASH分区

基于给定的分区个数，将数据分配到不同的分区，HASH分区只能针对整数进行HASH，对于非整形的字段只能通过表达式将其转换成整数。

##### 3: KEY分区

KEY分区其实跟HASH分区差不多，不同点如下：

1. KEY分区允许多列，而HASH分区只允许一列。

2. 如果在有主键或者唯一键的情况下，key中分区列可不指定，默认为主键或者唯一键，如果没有，则必须显性指定列。

3. KEY分区对象必须为列，而不能是基于列的表达式。

4. KEY分区和HASH分区的算法不一样，PARTITION BY HASH (expr)，MOD取值的对象是expr返回的值，而PARTITION BY KEY (column_list)，基于的是列的MD5值。

更多分区类型详情，请参考[分区表基本类型](http://mysql.taobao.org/monthly/2017/11/09/)

----
*后述：*

对分区表的使用有限，没有太多实战经验，因此这里就不谈使用场景等了，先把基础的知识记录下来，后面有更多的使用经验或心得，再来更新。
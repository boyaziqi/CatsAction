title: MySQL资料和问题汇总
date: 2018-06-16
category: MySQL

## 常见MySQL自省命令

1）查看索引信息

```mysql
show index from table;
```

2）查看当前用户占用的连接数

```mysql
show processlist;
show full processlist;
```

3）查看哪些事务正在执行

```mysql
# 运行中的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX;
# 锁定的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;
# 正等待的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;
```

4）查看当前连接数

```mysql
SHOW STATUS LIKE 'Thread_%';
```

## MySQL问题汇总

1）MySQL8用户创建和授权

之所以特意提及这点，是因为MySQL8对于不存在的用户是不允许的，必须先创建。而MySQL5.6之前的版本`grant`授权会自动创建用户。

2）”caching_sha2_password“认证插件不允许远程登录

MySQL8默认的认证插件是”caching_sha2_password“，需要改成”mysql_native_password“才能远程连接登录。修改方法如下。

```mysql
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
```

或者修改配置文件

```bash
[mysqld]
default_authentication_plugin = mysql_native_password
```

----------
参考资料
[MySQL监控命令](https://www.cnblogs.com/alan6/p/11589165.html)
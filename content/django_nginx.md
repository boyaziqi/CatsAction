title: Django项目部署实践一
subtitle: 基于MySQL读写分离和Nginx反向代理
date: 2018-04-15
category: Redis
tags: Redis, Python

从本篇开始，我会花三篇左右的文章去写写Django项目部署的演变及过程中的一些思考。在这个过程中，遇到了很多问题，我也会把相关问题和解决方法记录下来，以求更加完善Django架构解决方案。当然，架构没有最好，只有更适合。某些实现记录，我们也没这样做，这里写下只是为了做一下探索。探索中，难免遇到很多新理论和技术方案，我后面也会抽时间写相应的文章记录下来。

## 最基本的Django部署方案
Django作为Python最流行的Web框架，有很成熟的解决方案。作为MVT框架，它和数据库有很好的集成，类置ORM。下面是最基本的部署方案。

<center>
![django基本部署方案]({static}/images/django_deploy_semple.gif)
</center>

最基本的部署方案中，Nginx通过WSGI和Django通信，Django直接访问数据库。

##### 缺点
1. 高并发情况下有Django应用和数据库都会成为性能瓶颈；
2. 数据库只有一台，没有备份。如果服务器出问题，容易导致数据丢失；
3. 整个服务单点，出现故障就导致无法提供正常的访问。
<br>


## MySQL主从和负载均衡调度方案
基于基本部署方案并发性能低，无高可用。所以可以考虑Nginx负责均衡和MySQL主从读写分离。方案如下图。
<center>
![django负载均衡方案]({static}/images/django_junheng.gif)
</center>

上面的图MySQL只是一个基本的主从，当然实际情况可能还需要集群来解决数据不一致性问题。不过我们先一步步来，以最基本的两台数据库，一主一从，读写分离，展示下Django负载均衡调度的配置方案。下面的示例中展示忽略缓存，后面再讨论。

## Django负载均衡配置
1, 创建两个Django APP示例

为了展示负载均衡调度成功，我们创建两个Django应用，他们的/home路由对应下面的index view。第二个Django APP index view可以返回"this is the second home"，以便和第一个区别。
```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("this is the first home")
```
目前只是验证，所以Django APP直接`python manage.py runserver`启动。  
假设两个Django APP的地址分别为192.168.10.10：8000和192.168.10.11

2, 配置Nginx负载均衡调度
```nginx
upstream django-server {
    #least_conn;
    server 192.168.10.10:8000 weight=2;
    server 192.168.10.11:8000;
}

server {
    listen       80;
    server_name  localhost;
    location / {
        proxy_pass http://django-server;
    }
}
```
Nginx内置支持的负载均衡有round-robin（轮询，默认，可以指定权重），least-connected（最少链接数），ip-hash。为了验证结果，我们这里使用默认的round-robin, 两天服务器的访问权重是2:1。

3, 配置MySQL主从

假设MySQL主服务器ip为192.168.10.20，从服务器ip为192.168.10.21

MySQL主服务器配置文件增加下面配置
```mysql
[mysqld]
server-id=1
log-bin=mysql-bin
```
MySQL从服务器配置文件增加下面配置
```mysql
[mysqld]
server-id=2
relay_log=edu-mysql-relay-bin
```

其他配置项目不再列出，注意以下几点
- 主从配置项在[mysqld]，而不是[mysql_safe]
- server-id必须唯一
- 确保数据目录auto.cnf文件server-uuid也唯一，通常server-uuid会自动生成，但是有时拷贝数据会复制到，所以需要注意下。

在MySQL主服务器上新建主从复制专用用户
```
CREATE USER 'slave'@'%' IDENTIFIED BY '123456';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';
```
PS： MySQL8必须先创建用户才能授权，MySQL5.7以前版本可以直接grant创建用户并授权。后面会整理一篇MySQL8的文章。

在从服务器执行下面的命令
```mysql
change master to master_host='192.168.10.20', master_user='slave', master_password='123456', master_port=3306, master_log_file='mysql-bin.000001', master_log_pos= 2830, master_connect_retry=30;
```
master_host为主服务器ip，master_log_file和master_log_pos为主服务器`show master status`显示的File和Position值。

在从服务器开启主从复制
```mysql
mysql>start slave;
```

4, 配置Django支持读写分离

更新配置文件，指定多个数据库信息
```
DATABASES = {
    'default': {
        'NAME': 'write_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '123456'
    },
    'users': {
        'NAME': 'read_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}
```

指定读写分离路由
```python
class WriteReadRoute:
    def db_for_read(self, model, **hints):
        return read_db

    def db_for_write(self, model, **hints):
        return write_db
```

更新配置文件指定路由

```python
DATABASE_ROUTERS=['writeReadRoute']
```

## 读写分离的缺陷
1, 不能保证数据强一致性

MySQL主从复制采取异步的方式。主服务器先生存bin-log日志，然后传输给从服务器生存中继日志。中继日志生成后，MySQL从服务器会单独生成一个线程，用来更新数据库。由于是异步，MySQL主从复制存在一个数据不一致的时间差。

2, 写只在主服务器，读只在从服务器，不能充分利用多数据库的并发性能。

3, 不稳定，容易造成数据丢失。

4，可扩展性差。当需要增加主从服务器时，需要手动更新相关数据和配置。

## 结语
MySQL主从复制，读写分离搭建简单，对于小型应用，这样方案足够。但是当数据库增加时，管理及扩张及其不方便，而且数据也不能保证实时一致性。后面的文章会写写集群的解决方案。
基于Docker构建Redis主从复制和Sentinel哨兵
-------------------------------------

#### 使用方式
- 克隆仓库源，cd进入`examples/redis-replication`目录。
- 终端执行`docker-compose up`启动容器。

#### 说明
- sentinel.conf中主机名和端口，在Sentinel哨兵启动后，会被服务自动修改为一串hash值。克隆的本地后，需要先手动改为对应的主服务节点主机名。

- 需本地安装docker容器和docker-compose
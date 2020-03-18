title: Docker常见问题汇总
date: 2018-01-28
category: Docker
tags: Docker, containers 

##### docker容器没有ping命令

解决方法
```bash
sudo apt-get update && apt-get install iputils-ping
```

##### docker容器没有netstat，ifconfig命令

解决方法
```bash
sudo apt-get update && apt-get install net-tools
```

##### docker如何ping两个容器
...

##### Docker 拷贝容器文件到宿主机
使用`docker cp`命令，详情查看`docker help cp`
```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
```

##### CMD和ENTRYPOINT的区别
ENTRYPOINT启动的程序不会被docker run命令行指定的参数所覆盖，而且，这些命令行参数会被当作参数传递给ENTRYPOINT指定指定的程序。

##### Docker如何访问宿主机端口
假设一个Docker容器运行Nginx，而它想反向代理主机的Django应用，这种情况容器如何访问主机端口呢。第一种方式是把网络模式设置为hosts，这样主机和容器共享网络，但是打破了容器的隔离性。第二种方式：docker 18.03 加入了一个 feature，在容器中可以通过 host.docker.internal 来访问主机。

怎么查看容器IP
```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' 容器名称|容器id
docker inspect --format='{{.NetworkSettings.IPAddress}}' 容器名称| grep IPAddress
```
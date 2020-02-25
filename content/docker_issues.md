title: Docker常见问题
date: 2017-01-28
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
```bash
hh
```
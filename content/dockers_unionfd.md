title: Docker系列（二）
subtitle: 技术原理（UnionFS，Namespace，Cgroup）
date: 2017-12-01
category: Docker 
tags: UnionFS, aufs, overlay2, Device mapper, Docker

Docker是时下很流行的容器技术，它用到的技术主要是Cgroup，Namespace，UnionFS。

- Cgroup为​​​系​​​统​​​中​​​所​​​运​​​行​​​任​​​务​​​（进​​​程​​​）的​​​用​​​户​​​定​​​义​​​组​​​群​​​分​​​配​​​资​​​源​​，比​​​如​​​ CPU 时​​​间​​​、​​​系​​​统​​​内​​​存​​​、​​​网​​​络​​​带​​​宽​​​或​​​者​​​这​​​些​​​资​​​源​​​的​​​组​​​合​​​​。
- Namespace进行进程隔离，使容器拥有自己的rootfs和hostname。同时使IPC、网络和其他进程隔离。
- UnionFS打包容器运行时的各种依赖和库，发布成镜像。在容器启动时挂载成/目录，保证了容器运行的环境的统一，方便部署和管理。

![dockers_architecture]({static}/images/dockers_architecture.png)

#### Namespace
Linux Namespace是Linux提供的一种内核级别环境隔离的方法。Namespace提供如下功能。

- 把自身pid印射为0，并看不到其他任何的pid，这样自身的pid成为系统内唯一存在pid，看起来就像新启动了系统
- 用户名隔离，可以把用户名设置为“root”
- hostname隔离，可以另取一个hostname，成为新启动进程的hostname
- IPC隔离，隔离掉进程之间的互相通信
- 网络隔离，隔离掉进程和主机之间的网络 
- 可以自定义rootfs，比如我们把整个ubuntu发行版的可执行文件以及其他文件系统都放在目录/home/admin/ubuntu/下，当我们重定义rootfs = /home/admin/ubuntu后，则该文件地址被印射为"/"

如何基于Linux Namespace创建一个隔离的进程，可以参考[DOCKER基础技术：LINUX NAMESPACE](https://coolshell.cn/articles/17010.html)

#### Cgroup
Cgroups 是 Linux 内核提供的一种机制，这种机制可以根据特定的行为，把一系列系统任务及其子任务整合（或分隔）到按资源划分等级的不同组内，从而为系统资源管理提供一个统一的框架。<br>
通俗的来说，cgroups 可以限制、记录、隔离进程组所使用的物理资源（包括：CPU、memory、IO 等），为容器实现虚拟化提供了基本保证，是构建 Docker 等一系列虚拟化管理工具的基石。Cgoup的详细知识，可以查看陈皓的博客[DOCKER基础技术：LINUX CGROUP](https://coolshell.cn/articles/17049.html)

#### UnionFS
UnionFS是Union File System的简写。它可以把多个目录联和挂载到同一个目录下。而目录的物理位置是分开的。UnionFS允许只读和可读写目录并存，就是说可同时删除和增加内容。<br>
UnionFS应用的地方很多，比如在多个磁盘分区上合并不同文件系统的主目录，或把几张CD光盘合并成一个统一的光盘目录(归档)。另外，具有写时复制(copy-on-write)功能UnionFS
可以把只读和可读写文件系统合并在一起，虚拟上允许只读文件系统的修改可以保存到可写文件系统当中。 例如把一张CD/DVD和一个硬盘目录给联合mount在一起，然后，你就可以对这个只读的
CD/DVD上的文件进行修改（当然，修改的文件存于硬盘上的目录里）。
关于UnionFS的操作示例，可以查看[AUFS](https://coolshell.cn/articles/17061.html)。<br>
Docker最开始采用AUFS作为文件系统，但由于AUFS未并入Linux内核，考虑到兼容性问题，在Docker 0.7版本中引入了存储驱动， 目前，Docker支持AUFS、Btrfs、Device mapper、OverlayFS、ZFS五种存储驱动。可以使用`Docker info`查看。
```bash
xufan in ~ λ docker info
Client:
 Debug Mode: false

Server:
 Containers: 40
  Running: 39
  Paused: 0
  Stopped: 1
 Images: 16
 Server Version: 19.03.5
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Native Overlay Diff: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
```
上面是我MacOS系统的输出，使用的overlay2。Backing FIlesystem表明操作系统层面的文件系统使用的是extfs。
关于五种驱动的介绍和对比，可参考[Docker五种存储驱动原理及应用场景和性能测试对比](http://dockone.io/article/1513)

#### 常见UnionFS
- AUFS
- overlay

AUFS和Overlay都是联合文件系统，但AUFS有多层，而Overlay只有两层，所以在做写时复制操作时，如果文件比较大且存在比较低的层，则AUSF可能会慢一些。而且Overlay并入了linux kernel mainline，AUFS没有，所以可能会比AUFS快。

#### overlay和overlay2
overlay共享数据方式是通过硬连接，而overlay2是通过每层的lower文件。

#### docker的镜像rootfs，和layer的设计
为了让容器运行时一致，docker将依赖的操作系统、各种lib依赖整合打包在一起（即镜像），然后容器启动时，作为它的根目录（根文件系统rootfs），使得容器进程的各种依赖调用都在这个根目录里，这样就做到了环境的一致性。<br>
Docker镜像的设计中，引入了层（layer）的概念，用户制作镜像的每一步操作，都会生成一个层，也就是一个增量rootfs（一个目录）。下层作为上层的依赖，提供只读的环境。上层需要修改下层文件时，先复制一份到本层，修改发布后作为镜像成为其他容器的依赖。
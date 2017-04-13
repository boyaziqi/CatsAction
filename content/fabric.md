Title: 使用fabric远程部署代码
Date: 2016-05-03
Modified: 2017-04-13 14:13
category: python
tags: fab, 自动化运维

#### 1：安装
```shell
pip install fabric
```

#### 2：基本使用
在项目目录下新建fabfile.py文件，写入如下代码。fab的所有任务均写在fabfile.py文件或者fabfile包目录中（含有__init__.py）
```python
from fabric.api import *

def uname():
    local("uname -s")
```


#### 3：在远程机器上执行
在远程机器上执行，需要把local换成run。
```python
from fabric.api import *

def uname():
    run("uname -s")
```
```shell
$ fab uname
```
运行这个命令，会让你输入远程机器的名字。然后在指定的机器上执行uname -s

#### 4：指定主机
可以通过env.hosts指定。env是一个dict子类，可以像操作字典一样访问它，也可以想类一样直接访问它的属性。
```python
from fabric.api import env, run

env.hosts = ['host1', 'host2']

def mytask():
    run('ls /var/www')
```
可以通过命令行选项指定
```shell
$ fab -H host1,host2 mytask
```
*注意：命令行指定的主机会被env.hosts覆盖。可以通过env.hosts.extend(['host3', 'host4'])追加*   
可以给具体的某个任务指定主机，这样会更灵活*
```shell
$ fab mytask:hosts="host1;host2"
```
在fabfile文件你直接通过hosts装饰器给某个任务指定主机
```python
from fabric.api import hosts, run

@hosts('host1', 'host2')
def mytask():
    run('ls /var/www')
```
**注意：以上主机的定义的优先顺序为：fab mytask:host=host1，@hosts('host1')，env.hosts = ['host1']，--hosts=host1**

#### 5：定义远程主机角色组
```python
from fabric.api import env

env.roledefs = {
    'web': ['www1', 'www2', 'www3'],
        'dns': ['ns1', 'ns2']
        }

        @roles('web')
        def mytask():
            run('ls /var/www')
```
上面任务会在主机www1，www2，www3上执行

#### 6：定义排除的主机
使用--exclude-hosts/-x排除不想执行的主机。


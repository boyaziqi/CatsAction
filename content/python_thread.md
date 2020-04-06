title: Python进程、线程和协程
date: 2018-04-12
category: Python
tags: Python, 线程, 进程

## 前述

本篇会先讲解进程、线程和协成概念，并分别对比进程和线程、线程和协程的区别。然后会讲解进程的通信方式。最后，我们回到Python，讲解Python对协程、线程、进程的支持。以及Python对线程同步和进程同步的支持。

## 进程和线程

进程是程序运行时的一个实例，对Linux或其他类Unix系统来说，通过`ps`命令查看到的就是一些进程信息。

进程是系统资源分配的最小单位。对于每一个进程，操作系统都会维护一个进程控制块的结构（PCB）。在PCB中，维护着对应进程的标识、状态、调度标识、所拥有的资源、父子关系、进程间通信相关信息以及一些定时器信息。

由于每个进程拥有独立的PCB，因此一个进程是不能直接获取到另一个进程数据信息。如果多个进程需要交互数据信息，只能通过IPC（进程间通信）。常见的IPC方式有管道pipe、消息队列、共享存储、信号量、信号、套接字。

线程是操作系统的调度和运行的最小单位，它属于某一个具体的进程，是进程的实际执行单元。

如果一个进程开启了多个线程，那么这些线程共享所在进程资源信息，如地址空间，文件描述符，全局的变量。同一个进程的线程，可以通过操作共享的数据实现通信，但这样会导致数据的不一致。为了确保数据安全和避免不一致性，线程需要同步。常见的线程同步方式有互斥锁、条件变量、读写锁、信号量。

基于上面进程和线程的特点描述，进程和线程有如下几个对比特点。

- 进程是资源集合，线程是上下文执行单元。线程比较轻，进程比较重。

- 同一个进程的线程可以直接通信，但是多个进程之间通信只能通过IPC机制。

- 对主线程的修改可能影响其他线程，但是对父进程的修改（删除例外）不会影响其他子进程。

- 一个线程可以操作同一进程的其他线程，但是进程只能有限操作其子进程（这条特性待详细核定）。

*参考资料：*

*[Linux PCB属性](https://www.cnblogs.com/33debug/p/6705391.html)*

*[Linux进程控制块](https://blog.csdn.net/wangwenwen/article/details/8879375)*

*[进程的调度策略](https://blog.csdn.net/lanxinglan/article/details/41663607)*

*[linux线程剖析](https://blog.csdn.net/summy_j/article/details/72722853)*

*[Linux线程同步方式](https://www.cnblogs.com/yinbiao/p/11190336.html)*

## 线程和协程

协程，顾名思义，就是一些协同运行的程序或者对象。线程是操作系统的概念，而协程是用户编程层面的概念。线程的调度由操作系统控制，而协程由用户自己实现的事件循环调度。**协程强调的是异步，而线程（或者进程）强调的是并发**。对于Python来说，协程只是一种语法糖，一种异步任务的包装，让程序员写同步代码的方式来写异步任务代码。

## 进程间通信方式
1）管道pipe：管道是一种半双工的通信方式，数据只能单向流动，而且只能在具有亲缘关系的进程间使用。进程的亲缘关系通常是指父子进程关系。

2）命名管道FIFO：有名管道也是半双工的通信方式，但是它允许无亲缘关系进程间的通信。

3）消息队列MessageQueue：消息队列是由消息的链表，存放在内核中并由消息队列标识符标识。消息队列克服了信号传递信息少、管道只能承载无格式字节流以及缓冲区大小受限等缺点。

4）共享存储SharedMemory：共享内存就是映射一段能被其他进程所访问的内存，这段共享内存由一个进程创建，但多个进程都可以访问。共享内存是最快的IPC方式，它是针对其他进程间通信方式运行效率低而专门设计的。它往往与其他通信机制，如信号量配合使用，来实现进程间的同步和通信。

5）信号量Semaphore：信号量是一个计数器，可以用来控制多个进程对共享资源的访问。它常作为一种锁机制，防止某进程正在访问共享资源时，其他进程也访问该资源。因此，主要作为进程间以及同一进程内不同线程之间的同步手段。

6）套接字Socket：套解口也是一种进程间通信机制，与其他通信机制不同的是，它可用于不同及其间的进程通信。

7）信号 ( sinal ) ： 信号是一种比较复杂的通信方式，用于通知接收进程某个事件已经发生。

*参考资料：*

*[进程间通信方式](https://www.cnblogs.com/LUO77/p/5816326.html)*

## Python的协程

Python的协程是异步任务的包装，让程序员可以用写同步代码的方式写异步代码，而协程的调度需要事件循环的支持。Python标准库内置了事件循环库`asyncio`。

在Python中，实现协成有两种方式：Python3.5之前的生成器协成，Python3.5及以后的`async`和`await`关键字。

生成器协程
```Python
@asyncio.coroutine
def old_style_coroutine():
    print("hello")
    yield from asyncio.sleep(1)
    print("world")

loop = asyncio.get_event_loop()
loop.run_until_complete(old_style_coroutine())
```

基于`async`、`await`的原生协程
```Python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
Python3.7及以后的版本中加入了run来运行协成，会自动获取事件。Python3.7之前的版本则需要手动获取事件，然后调用`run_until_complete`等函数执行协程。

`asyncio`运行协程时，协程对象被包装成一个`asyncio.Task`对象（waitable对象），`Task`对象管理协程的状态和结果，协程运行结束可以通过`Task`对象的`result`方法获取结果。

*协程的更多信息可以参考官方文档和下面的资料*

*[asyncio](https://www.jianshu.com/p/b5e347b3a17c)*

*[async/await](https://zhuanlan.zhihu.com/p/27258289)*

## Python的线程

Python线程有两种实现方式：通过threading模块直接启动，或者继承Thread类实现线程。

通过treading模块直接启动
```Python
# 创建两个线程
import threading
import time


def task(name, delay):
    print(f"{name} started at {time.strftime('%X')}")
    time.sleep(delay)
    print(f"{name} finished at {time.strftime('%X')}")


t1 = threading.Thread(target=task, args=("t1", 2))
t2 = threading.Thread(target=task, args=("t2", 1))

t1.start()
t2.start()
```

下面是运行结果，可以看出同时启动，但是t2在t1前面结束，因为它只阻塞了疫苗。

```bash
t1 started at 16:56:43
t2 started at 16:56:43
t2 finished at 16:56:44
t1 finished at 16:56:45
```

继承`Thread`类实现线程
```python
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()  # 重构run函数必须要写
        self.name = name

    def run(self):
        print(f"{self.name} started at {time.strftime('%X')}")
        time.sleep(1)
        print(f"{self.name} finished at {time.strftime('%X')}")

if __name__ == "__main__":
    t1 = MyThread("t1")
    t2 = MyThread("t2")

    t1.start()
    t2.start()
```

下面是上面代码的运行结果
```bash
t1 started at 17:03:00
t2 started at 17:03:00
t1 finished at 17:03:01
t2 finished at 17:03:01
```
我们看到开始结束时间都是一致的，这每个人的显示可能不一致，取决于你的机器和系统。如果单核，阻塞时间很长，那结束时间可能不一致。

*关于Python线程及它们的同步, 参考*
[搞定Python进程和线程](https://www.cnblogs.com/whatisfantasy/p/6440585.html)

我们知道线程同步可以通过互斥锁，条件变量，信号量。`threading`库对它们支持的对象分别为`Lock`、`Condition`、`Semaphore`。除了这些，`threading`库还支持其他同步对象，如`Even`, `Barrier`。

## Python的进程

Python进程由三种实现方式：基于multiprocessing、继承Process类和进程池Pool。

通过multiprocessing直接启动

```Python
from multiprocessing import Process
import time
def f(name):
    time.sleep(2)
    print('hello', name)
 
if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

继承Process类

```Python
class SubProcess(Process):
    def __init__(self, interval, name=None):
        super().__init__()
        self.interval = interval
        if is not None:
            self.name = name

    def run(self):
        print("子进程(%s)开始执行，父进程为(%s) " % (os.getpid(), os.getppid()))

        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print("子进程(%s )执行结束，耗时%0 .2f秒" % (os.getpid(), t_stop - t_start))
```

进程池Pool

```Python
rom  multiprocessing import Process,Pool
import time
 
def Foo(i):
    time.sleep(2)
    return i+100
 
def Bar(arg):
    print('-->exec done:',arg)
 
pool = Pool(5)  #允许进程池同时放入5个进程
 
for i in range(10):
    #func子进程执行完后，才会执行callback，否则callback不执行（而且callback是由父进程来执行了）
    pool.apply_async(func=Foo, args=(i,),callback=Bar)
    #pool.apply(func=Foo, args=(i,))
 
print('end')
pool.close()
pool.join() #主进程等待所有子进程执行完毕。必须在close()或terminate()之后
```

Python的multiprocessing库提供了如下对象支持进程间通信：`Queue`、`Pipe`、`Manager`、共享内存（Value, Array）等，也支持如线程同步的`Lock`等同步对象。

*更多Python进程信息，可以参考资料：*
[Python进程和线程](https://blog.csdn.net/xw1680/article/details/104442017)

## 后述

协程是Python3.4以后的一个概念，也是异步编程的一种趋势。网上很多关于协程和线程的对比的文章，什么协程更轻更快啥的，我觉得都只是看表象说理，没有体会协程的哲理。

线程和协程的区别，面试的时候经常问。我总结的协程和线程区别，也许并不全面，如果你有很好的看法，欢迎在[issue](https://github.com/boyaziqi/CatsAction/issues/15)留言。
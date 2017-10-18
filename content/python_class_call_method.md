Title: python类特殊方法__call__
Date: 2017-06-06 22:42:00
category: python
tags: __call__

当一个类实现了__call__方法时，它的*实例*就是可调用的。即像函数一样使用。
```python
class CallTest(object):
    def __init__(self, name):
        print(name)

    def __call__(self, x, y):
        print("sum:", x+y)
``` 
```shell
t = CallTest("test")
t(1,2)
```

上面将会输出:
```shell
test
sum: 3
```
从输出结果我们可以看到，__init__在创建实例的时候被调用，用来初始化一些属性。而__call__在实例被像函数一样调用时被调用。

####总结:   
python3中，类是type的实例，用dir(type)查看type的方法时，可以看见type实现了__call__方法，因此在定义类的时候会调用对应的__call__方法，这也是
元类的工作方式。关于元类，可以查看我的其他文章。同样，函数也实现了__call__方法

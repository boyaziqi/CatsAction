Title: weakref使用与理解
Date: 2015-08-30
Modified: 2017-04-14 10:38
category: python
tags: weakref, 弱引用

python weakref模块的使用 
python的垃圾回收器，最主要的一种方式是引用计数，就是当某个对象的引用为0时，该对象将被回收。不过引用计数最大的缺点就是无法解决循环引用的问题。   
weakref可以实现弱引用，弱引用和普通引用的区别是：当某个对象只存在弱引用时，它会被垃圾回收器收回。 通常用来创建缓存对象和对大型对象的引用。    

#### 使用    
```python
import weakref
class Object(object):
    pass

o = Object()
r = weakref.ref(o)

o2 = r()
if 02 is None:
    print("object has been deleted")
else:
    print("do something")
```
由于弱引用会被删除，通常都需要判断它是否存在。当然，如果引用对象是一个类，你可以用hasattr检查它是否有某个属性。None当然没有对应的属性。
```python
import weakref
class WeakObject(object):
    pass

r = weakref.proxy(WeakObject)
if hasattr(r, "name"):
    r.name
```
这里r不是弱引用对象，而是相应对象的弱引用。

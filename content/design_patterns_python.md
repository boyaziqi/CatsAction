Title: Python 设计模式总结
Date: 2016-03-10 22:52
category: python
tags: 设计模式

### 单例模式
```python
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_insurance'):
            cls._insurance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)

        return cls._insurance


if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    print(s1)
    print(s2)
```

输出结果

```bash
<__main__.Singleton object at 0x1019f6320>
<__main__.Singleton object at 0x1019f6320>
```
每个人的输出结果可能不一样，但他们应当相等

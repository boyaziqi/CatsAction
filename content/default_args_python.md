Title: Python 默认参数
Date: 2018-03-22 11:56
category: python
tags: default arg

python 默认值的陷阱

```python
def test(a, l = []):
    for i in range(a):
        l.append(i)
    print(l)
```
```python
>>> test(2)
>>> test(2, [1])
>>> test(3)
```
输出结果
```python
[0, 1]
[1, 0, 1]
[0, 1, 0, 1, 2]
```

最后一行为什么是`[0, 1, 0, 1, 2]`, 而不是期望中的`[0, 1, 2]` ？<br>
官方文档是这样解释的
> Default values are computed once, then re-used.

因为默认值在函数定义的时候被初始化，而且只初始化一次, 后面重复使用。又因为列表可变的，顾不指定默认值的时候会不断的追加到默认值列表中。

Title: Go 的方法申明总结
Date: 2016-02-17
Modified: 2018-02-17
category: golang
tags: Go 面向对象


_下面的代码均省略包导入和主函数，只列出说明代码_

#### 1：不能为非本地类型申明方法
```go
func (i int) add (j int) int {
    return i + j
}
```

_如果运行上面的代码，会报错`cannot define new methods on non-local type int`，正确的写法是先将 int 类型申明为本地类型_
```go
type LocalInt int
func (i *LocalInt) add (j LocalInt) LocalInt {
    return *i + j
}
```
> 之所以申明为指针类型接受者，是为了方便后面讲解

### 2：类型字面量，不能直接调用指针接受者方法，必须先申明变量
```go
LocalInt(12).add(LocalInt(12))
```
_运行上面的代码，会如下错_
```shell
# command-line-arguments
./test.go:28:17: cannot call pointer method on LocalInt(12)
./test.go:28:17: cannot take the address of LocalInt(12)
```
_应先申明变量_
```go
i := LocalInt(12)
i.add(LocalInt(12))
```

### 3：go为强类型，相关类型不能混用
```go
i := 12
i.add(LocalInt(12))
```
_虽然 LocalInt 和 int 类型表现一致，但它们仍不是同一种类型，因此会报错`i.add undefined (type int has no field or method add)`_

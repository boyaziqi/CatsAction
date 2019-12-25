Title: Go 相关特性总结
Date: 2016-02-17
Modified: 2018-02-17
category: golang
tags: go基础

#### GO语言特点
- 类C语言，语法简单，关键字很少, 只有25个，学习入门很快。
- 编码风格强制性检测，让GO代码保持一致，易于阅读。
- 静态语言，但是有动态语言的感觉。比如var定义。
- 语言层面支持并发。
- 内置丰富的工具。比如gofmt格式化代码等。
- 跨平台编译，如果你写的Go代码不包含cgo，那么就可以做到window系统编译linux的应用，如何做到的呢？Go引用了plan9的代码，这就是不依赖系统的信息。
- 没有类，没有继承。
- 接口风格是鸭子风格，结构体实现了相关方法就实现了接口，不需要关键字来绑定。 
- 内置垃圾回收机制。
- 方法申明显示的指定接收者。

#### GO垃圾回收机制
go垃圾回收机制采用三色标记法https://juejin.im/post/5d56b47a5188250541792ede

#### 接口风格
下面的file结构体实现了stream接口，可以将file实例赋值给stream接口变量。
```go
// 接口申明
type stream interface{
    write(s string) int
}
type file struct {
    name string
}
func (f file) write(s string) int{
    fmt.Printf("write data stream: %s", s)
    return len(s)
}
var st stream
st = file{name: "test"}
```

#### 1：不能为结构体字面量直接赋值
```go
type Point struct {
    x int
    y int
}
// 错误
Point{1, 2}.x = 12

// 正确
var p = Point{1, 2}
p.x = 12
fmt.Println(p)
```
> 查看相关文档，总结出来的规律是不能为不能取地址的字面量赋值，因为还没赋值给变量，不能获取相关地址，指向不明确

#### 2：map 类型的元素不能直接取地址

_官方的解释是元素可能因为 map 大小的改变重新映射，导致地址改变_
```go
type Point struct {
    x int
    y int
}

var l = map[string]Point {
    "member": Point{1, 2},
}

// 错误
l["member"].x = 10

// 正确
p = l["member"]
p.x = 12
l["member"] = p
fmt.Println(l)
```
> 因为 struct 类型的获取，总是会隐式转化为指针访问，随意直接通过 map 元素访问会报错，赋值给变量明确指向

Title: Go 相关特性总结
Date: 2018-02-17
Modified: 2018-02-17
category: golang
tags: go基础

### 1：不能为结构体字面量直接赋值
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

### 2：map 类型的元素不能直接取地址

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

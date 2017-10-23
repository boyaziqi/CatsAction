Title: python inspect模块
Date: 2015-05-10
Modified: 2017-04-13 15:39
category: python
tags: inspect

inspect模块可以用来作为python代码自省使用。

它的方法列举如下，详细使用方法见官方文档[inspect](https://docs.python.org/3/library/inspect.html)

getmembers  
getmodulename   
ismodule    
ismethod    


下面是一些检查对象定义的方法:   
getfile(object) 
getsource(object)   

class signature(callable, *, follow_wrapped=True)   
这个类可以用来检测函数签名  


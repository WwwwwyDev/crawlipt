---
description: crawlipt提供了check和alias两个装饰器来控制action以及condition方法
---

# Annotation

### check 装饰器

check装饰器用来对函数调用时进行参数检查，如果调用时参数不符合类型，则抛出异常。使用check装饰器可以增强脚本检查，以及避免脚本执行由于参数类型非法导致的错误。exclude参数意味着你将排除这几个参数的检查。

```python
import crawlipt as cpt

@cpt.check(exclude=["a","b"])
def A(a:str,b:int,c:float):
    pass
```

### alias 装饰器

alias装饰器可以为你添加的action以及condition方法添加一个别名，脚本可以通过别名映射到函数。

```python
import crawlipt as cpt

@cpt.alias(name="B")
def A(a:str,b:int,c:float):
    pass
```

---
description: 存储器贯穿在脚本执行的全过程，帮助你在脚本执行过程中收集和存储信息
---

# Store

### 实现Store

在使用Store前，你需要实现一个存储类，继承自StoreBase，里面定义你自己的存储变量。当你实现set方法时（也可以不实现），在脚本执行过程中，如果某个action方法的返回值不为空值，则会自动调用set方法，传入方法名以及对应的返回值。

```python
import crawlipt as cpt
class Store(cpt.StoreBase):

    @check
    def __init__(self, is_replace: bool = False):
        """
        :param is_replace: need replace the value of method or not
        """
        self.is_replace = is_replace
        self.data = {}

    @check
    def set(self, method: str, value: Any) -> None:
        if method in self.data.keys():
            if self.is_replace:
                self.data[method] = value
            else:
                self.data[method].append(value)
            return
        if self.is_replace:
            self.data[method] = value
        else:
            self.data[method] = [value]
```

上述实现已在crawlipt中内置

### 内置Store对象

```python
import crawlipt as cpt
loader = cpt.Script(step, interval=3)
s = cpt.Store(is_replace=False)  # 是否需要替换
loader.process(webdriver, store=s)
print(s.data)  # 会自动收集所有非空返回值
```

### 使用Store

Store需要在你自己定义的[action](actions.md#tian-jia-ni-zi-ji-de-action)或者[condition](condition.md#tian-jia-ni-zi-ji-de-condition)中作为参数传入

```python
"""
（1）变量名必须为store，否则无法传入
（2）你需要排除store的语法检查，否则无法通过
（3）store和driver均为特殊参数，在你自己实现的condition以及action中不能存在同名参数
"""
@cpt.check(exclude=["driver", "store"]) 
def myAction_or_myCondition(driver: WebDriver, store: MyStore, limit: int) -> Any:
    store.data.append(1)

store = MyStore()
cpt.Script.add_action(myAction_or_myCondition)
step = [...]
# cpt.Script.add_condition(myAction_or_myCondition)
loader = cpt.Script(step, interval=1)
# 在执行期间传入store
loader.process(webdriver=webdriver, store=store)
print(store.data)
webdriver.quit()
```

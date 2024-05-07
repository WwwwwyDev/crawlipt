---
description: 存储器贯穿在脚本执行的全过程，帮助你在脚本执行过程中收集存储信息
---

# 🐻 Store

### 实现Store

在使用Store前，你需要实现一个存储类，继承自StoreBase，里面定义你自己的存储变量

```python
import crawlipt as cpt
class MyStore(cpt.StoreBase):
     def __init__(self):
         self.data = []
```

###  使用Store

Store需要在你自己定义的action或者condition中作为参数传入

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


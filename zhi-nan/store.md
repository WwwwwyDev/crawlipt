---
description: >-
  Memory runs through the entire process of script execution, helping you
  collect and store information during the script execution process
---

# Store

### Implement Store

Before using Store, you need to implement a storage class that inherits from StoreBase and defines your own storage variables. When you implement the set method (or not), during script execution, if the return value of an action method is not null, the set method will be automatically called, with the method name and corresponding return value passed in.

```python
import crawlipt as cpt
class Store(cpt.StoreBase):

    def __init__(self, is_replace=False):
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

The above implementation is already built-in in crawlipt

### Built-in Store object

```python
import crawlipt as cpt
loader = cpt.Script(step, interval=3)
s = cpt.Store(is_replace=False)  # Do you need to replace it
loader.process(webdriver, store=s)
print(s.data)  # Will automatically collect all non empty return values
```

### Using Store

Store needs to be passed as a parameter in your own defined [action](actions.md#tian-jia-ni-zi-ji-de-action) or [condition](condition.md#tian-jia-ni-zi-ji-de-condition)

```python
"""
(1) The variable name must be store, otherwise it cannot be passed in
(2) You need to exclude the syntax check of the store, otherwise it will not pass
(3) Both store and driver are special parameters, and parameters with the same name cannot exist in your own implemented conditions and actions
"""
@cpt.check(exclude=["driver", "store"]) 
def myAction_or_myCondition(driver: WebDriver, store: MyStore, limit: int) -> Any:
    store.data.append(1)

store = MyStore()
cpt.Script.add_action(myAction_or_myCondition)
step = [...]
# cpt.Script.add_condition(myAction_or_myCondition)
loader = cpt.Script(step, interval=1)
# Pass in store during execution
loader.process(webdriver=webdriver, store=store)
print(store.data)
webdriver.quit()
```

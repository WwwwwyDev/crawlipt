---
description: 变量可以增强脚本的灵活性以及扩展性，可以动态控制脚本的运行
---

# Variable

### 脚本示例

变量可以设置在脚本的任意参数中（除"method", "next", "if", "check", "condition", "loop"关键词)

```json
step = [{
    "method": "redirect",
    "url": "https://www.baidu.com/",
}, {
    "method": "input",
    "xpath": "//*[@id=\"kw\"]",
    "text": "__v-searchKey__",
    "if": {
        "condition": "presence",
        "xpath": "__v-button_xpath__"
    }
}, {
    "method": "clear"
}]
```

在编写脚本变量时，需要以"\_\_v-"开头，以及以"\_\_"结尾。即"\_\_v-{your variable}\_\_"。否则在语法检查时会被判断为普通参数处理。

### variable对象

脚本中的变量会在执行期间被自动替换，你可以创建crawlipt内置的Variable对象，初始化参数为字典或者json格式字符串。字典中需要将你的变量名以及值一一对应，在执行期间会替换脚本中的变量名为你设置的变量值。

```python
import crawlipt as cpt
v = cpt.Variable({
            "searchKey": "hello",
            "button_xpath": "//*[@id=\"su\"]"
        })
loader = cpt.Script(step, interval=3)
loader.process(webdriver=webdriver,
               variable=v) # 在执行阶段传入变量对象
```

### 实现你自己的variable对象

你需要继承VariableBase对象，并且实现get、\_\_contains\_\_ 这两个方法

```python
import crawlipt as cpt
class Variable(cpt.VariableBase):
    @cpt.check
    def __init__(self, values: dict | str):
        if isinstance(values, str):
            values: dict = json.load(values)
        self.values = values

    @cpt.check
    def get(self, key: str) -> Any:
        return self.values.get(key)

    @cpt.check
    def __contains__(self, key: str):
        return key in self.values
```

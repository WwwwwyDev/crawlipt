---
description: >-
  Variables can enhance the flexibility and scalability of scripts, and can
  dynamically control the running of scripts.
---

# Variable

### Script Example

Variables can be set in any parameter of the script (except for keywords such as "method", "next", "if", "check", "condition", and "loop").

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

When writing script variables, the identifier "\_v - {your variable} \_\_" needs to be used. Otherwise, it will be judged as a normal parameter processing during syntax checking.

### Implement your own variable object

You need to inherit the VariableBase object and implement the "get" and "\_\_ contains\_\_" methods.

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

The above implementation is already built-in in crawlipt.

### Built-in variable object

The variables in the script will be automatically replaced during execution, and you can create a built-in Variable object in crawlipt with initialization parameters in dictionary or JSON format strings. The dictionary needs to correspond your variable names and values one-to-one, and during execution, it will replace the variable names in the script with the variable values you set.

```python
import crawlipt as cpt
v = cpt.Variable({
            "searchKey": "hello",
            "button_xpath": "//*[@id=\"su\"]"
        })
loader = cpt.Script(step, interval=3)
loader.process(webdriver=webdriver,
               variable=v) # Passing in variable objects during the execution phase
```

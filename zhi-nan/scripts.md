---
description: This chapter introduces the basic use of scripts. The script is defined in JSON format and can be easily deserialized in various languages.
---

# Script

### 转换方式

```python
import crawlipt as cpt

# During the writing phase, Python built-in dictionary types can be used for writing
script = { 
    "method": "redirect",
    "url": "https://www.baidu.com/",
    "next": {
        "method": "input",  # Method name
        "xpath": "//*[@id=\"kw\"]", # Method corresponding parameters
        "text": "百度贴吧", # Method corresponding parameters
        "next": { # Next script to execute
            "method": "click",
            "xpath": "//*[@id=\"su\"]"
        }
    }
}
# Convert to a JSON string, which can be stored in a physical medium
script_json = cpt.Script.generate_json(script) 
```

### 执行脚本

脚本可以映射所有的action方法

```python
webdriver = getDriver()
# Pass in a pre written script that supports JSON strings, Python dictionaries, and list types
loader = cpt.Script(script, interval=0.1)
# Pass in the webdriver object of your configured selenium for execution
loader.process(webdriver) 
# loader(webdriver) 
# You need to close your webdriver after execution
webdriver.quit()
```

### 脚本初始化参数介绍

| 参数名                     | 类型                         | 介绍                                                                                                       |
| ----------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------- |
| script                  | dict \| str \| list        | 预先编写好的脚本                                                                                                 |
| global\_script          | dict \| str \| list = None | 全局执行脚本，这个脚本将在每次执行任意一个action方法前进行执行。例如：有的网站会随机弹出广告，影响下面脚本的执行，定义该脚本可以在执行action方法前判断是否有广告，如果有的话去进行一系列操作关闭广告 |
| interval                | float = 0.5                | 每两次action方法执行的间隔                                                                                         |
| wait                    | float = 10                 | 如果action方法中含有xpath或css参数，则会自动隐式等待wait秒，直到对应元素在dom结构中出现                                                   |
| is\_need\_syntax\_check | bool = True                | 是否需要执行前严格的脚本语法检查，如果关闭会增加执行时的错误概率                                                                         |

### 脚本执行器参数介绍

| 参数名                                                                    | 类型                          | 介绍                              |
| ---------------------------------------------------------------------- | --------------------------- | ------------------------------- |
| [webdriver](https://www.selenium.dev/documentation/webdriver/drivers/) | WebDriver                   | selenium的webdriver对象，需要根据情况自行配置 |
| [variable](variable.md)                                                | VariableBase \| None = None | 本次执行的变量值                        |
| [store](store.md)                                                      | StoreBase \| None = None    | 本次执行的存储器                        |

### 通过列表step方式编写脚本

Writing scripts using dictionary types may result in nested dictionaries being too deep and difficult to maintain in situations with multiple actions. Writing scripts using a list approach can turn nested processes into serial processes.

```python
step = [{
            "method": "redirect",
            "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"editor-text\"]/div[1]/div[1]/div/div/div/div",
            "text": "Hello, World",
        }, {
            "method": "getInnerText",
            "xpath": "//*[@id=\"trans-selection\"]/div/span",
        }]

# You can use generate to convert the list script into a dictionary script
script_dict = cpt.Script.generate(step)
# You can use generate_JSON to directly convert the list script into a JSON string
script_json = cpt.Script.generate_json(step)
# Executors can also directly execute list scripts
loader = cpt.Script(step, interval=0.1)
loader.process(webdriver) 
```

---
description: 本章介绍脚本的基本使用。脚本使用json格式定义，在各种语言中，你都可以很方便将它反序列化。
---

# Script

### 转换方式

```python
import crawlipt as cpt

# 在编写阶段可以使用python内置字典类型进行编写
script = { 
    "method": "redirect",
    "url": "https://www.baidu.com/",
    "next": {
        "method": "input",  # 方法名
        "xpath": "//*[@id=\"kw\"]", # 方法对应参数
        "text": "百度贴吧", # 方法对应参数
        "next": { # 下一个要执行的脚本
            "method": "click",
            "xpath": "//*[@id=\"su\"]"
        }
    }
}
# 转换为了一个json字符串，可以将它存储在物理介质中
script_json = cpt.Script.generate_json(script) 
```

### 执行脚本

脚本可以映射所有的action方法

```python
webdriver = getDriver()
# 传入一个预先编写好的脚本，支持json字符串，python字典、列表类型
loader = cpt.Script(script, interval=0.1)
# 传入你配置好的selenium的webdriver对象进行执行
loader.process(webdriver) 
# loader(webdriver) 
# 你需要关闭你的webdriver在执行后
webdriver.quit()
```

### 脚本执行器参数介绍

| 参数名                     | 类型                         | 介绍                                                                                                       |
| ----------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------- |
| script                  | dict \| str \| list        | 预先编写好的脚本                                                                                                 |
| global\_script          | dict \| str \| list = None | 全局执行脚本，这个脚本将在每次执行任意一个action方法前进行执行。例如：有的网站会随机弹出广告，影响下面脚本的执行，定义该脚本可以在执行action方法前判断是否有广告，如果有的话去进行一系列操作关闭广告 |
| interval                | float = 0.5                | 每两次action方法执行的间隔                                                                                         |
| wait                    | float = 10                 | 最长等待xpath对应元素出现的时间                                                                                       |
| is\_need\_syntax\_check | bool = True                | 是否需要执行前严格的脚本语法检查，如果关闭会增加执行时的错误概率                                                                         |

### 通过列表step方式编写脚本

通过字典类型进行编写脚本，在action多的情况下，可能会导致嵌套字典过深，维护困难。使用列表方式编写脚本可以将嵌套流程变为串行流程。

```python
step = [{
            "method": "redirect",
            "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"editor-text\"]/div[1]/div[1]/div/div/div/div",
            "text": "你好，世界",
        }, {
            "method": "getInnerText",
            "xpath": "//*[@id=\"trans-selection\"]/div/span",
        }]

# 你可以使用generate，将列表脚本变为字典脚本
script_dict = cpt.Script.generate(step)
# 你可以使用generate_json，将列表脚本直接变为json字符串
script_json = cpt.Script.generate_json(step)
# 执行器也可以直接执行列表脚本
loader = cpt.Script(step, interval=0.1)
loader.process(webdriver) 
```

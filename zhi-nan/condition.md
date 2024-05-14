---
description: crawlipt包含了一些内置的condition，以便你在与网页进行交互可以进行一些逻辑判断。同时你也可以添加自己的condition方法，进行扩展。
---

# Condition

### 内置的condition方法

与action方法不同，condition方法的返回值均为bool类型，你可以在[while](loop.md#loop-tiao-jian)、[if](judge.md#if-guan-jian-ci)、[check](judge.md#check-guan-jian-ci)中使用它。

<table><thead><tr><th width="122">方法</th><th>别名</th><th>参数</th><th>备注</th></tr></thead><tbody><tr><td>presence_of_element_located</td><td>presence</td><td><p>xpath: str, </p><p>wait: float = 1(最长等待xpath对应元素出现时间)</p></td><td>判断xpath对应单个元素是否在wait时间内出现在dom结构中</td></tr><tr><td>presence_of_all_elements_located</td><td>presences</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应所有元素是否在wait时间内出现在dom结构中</td></tr><tr><td>visibility_of_element_located</td><td>visibility</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应单个元素是否在wait时间内出现在dom结构中，并且宽和高均不为0</td></tr><tr><td>invisibility_of_element_located</td><td>invisibility</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应单个元素是否在wait时间内出现在dom结构中，并且宽和高均为0</td></tr><tr><td>frame_to_be_available_and_switch_to_it</td><td>None</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应的frame是否能在wait时间内被切入</td></tr><tr><td>element_to_be_clickable</td><td>clickable</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应的单个元素是否能在wait时间内被点击</td></tr><tr><td>element_located_to_be_selected</td><td>selected</td><td><p>xpath: str, </p><p>wait: float = 1</p></td><td>判断xpath对应的单个元素是否能在wait时间内被选择</td></tr><tr><td>text_to_be_present_in_element</td><td>None</td><td><p>xpath: str, </p><p>text: str, </p><p>wait: float = 1</p></td><td>判断xpath对应的单个元素是否能在wait时间内出现text文本内容</td></tr><tr><td>text_to_be_present_in_element_value</td><td>None</td><td><p>xpath: str, </p><p>value: str, </p><p>wait: float = 1</p></td><td>判断xpath对应的单个元素的value中是否能在wait时间内出现value文本内容</td></tr><tr><td>alert_is_present</td><td>None</td><td>wait: float = 1</td><td>判断是否有alert弹出</td></tr></tbody></table>

### fail\_script关键词

在condition中如果含有fail\_script关键词，则在condition失败后会执行该脚本

```json
{
    "check": {
        "condition": "presence",
        "xpath": "//*[@id=\"main-metro\"]/ul/li[3]/a[3]",
        "fail_script": [{
            "method": "log",
            "msg": "[fail] 登录失败"
        }]
    }
}
```

### 逻辑取反

使用\_\_not-{your condition}\_\_指令可以对condition结果进行取反

```json
{
    "check": {
        "condition": "__not-presence__",
        "xpath": "//*[@id=\"main-metro\"]/ul/li[3]/a[3]",
        "fail_script": [{
            "method": "log",
            "msg": "[fail] 登录失败"
        }]
    }
}
```

### 添加你自己的condition

在你添加自己的action方法前，建议你先学习一下selenium的基本使用

{% embed url="https://www.selenium.dev/" %}

请参考下面的示例

```python
import crawlipt as cpt
from selenium.webdriver.remote.webdriver import WebDriver
"""
（1）必须为一个可调用的函数或者类内的静态方法
（2）必须使用check注解，来排除driver的语法检查，否则在语法检查阶段会抛出异常
（3）所有的参数必须注明类型，否则无法通过语法检查
（4）所有参数必须为python的基础类型
（5）必须注明函数返回值,且返回值类型必须为bool类型
（6）driver是固定变量，即必须包含(driver: WebDriver)这个参数
"""
@cpt.check(exclude="driver")  
def myConditon(driver: WebDriver, **args) -> bool:
    """
    your doc
    :param driver: selenium webdriver
    :param **args: your args
    """
    # write your code
    if ...:
        return True
    else:
        return False

# 按照如下方式添加脚本
cpt.Script.add_condition(myConditon)
```

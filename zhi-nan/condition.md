---
description: Crawlipt includes some built-in conditions so that you can make logical judgments when interacting with web pages. At the same time, you can also add your own condition method for extension.
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

Before adding your own action method, it is recommended that you first learn the basic usage of selenium

{% embed url="https://www.selenium.dev/" %}

Please refer to the following example

```python
import crawlipt as cpt
from selenium.webdriver.remote.webdriver import WebDriver
"""
(1) Must be a callable function or static method within a class
(2) The check annotation must be used to exclude the syntax check of the driver, otherwise an exception will be thrown during the syntax check phase
(3) All parameters must indicate the type, otherwise they cannot pass the syntax check
(4) All parameters must be of the underlying type in Python
(5) The function return value must be specified, and the return value type must be bool type
(6) Driver is a fixed variable, which means it must include the parameter (driver: WebDriver)
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

# Add the script as follows
cpt.Script.add_condition(myConditon)
```

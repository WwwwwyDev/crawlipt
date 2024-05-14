---
description: >-
  Crawlipt includes some built-in conditions so that you can make logical
  judgments when interacting with web pages. At the same time, you can also add
  your own condition method for extension.
---

# Condition

### Built-in condition method

Unlike the action method, the return value of the condition method is of type bool, which you can use in [while](loop.md#loop-tiao-jian), [if](judge.md#if-guan-jian-ci), and [check](judge.md#check-guan-jian-ci).

<table><thead><tr><th width="122">method</th><th>alias</th><th>parms</th><th>notes</th></tr></thead><tbody><tr><td>presence_of_element_located</td><td>presence</td><td><p>xpath: str,</p><p>wait: float = 1(The longest waiting time for the appearance of the corresponding element in xpath)</p></td><td>Determine whether a single element corresponding to xpath appears in the dom structure within the wait time</td></tr><tr><td>presence_of_all_elements_located</td><td>presences</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether all elements corresponding to xpath appear in the dom structure within the wait time</td></tr><tr><td>visibility_of_element_located</td><td>visibility</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether a single element corresponding to xpath appears in the dom structure within the wait time, and whether the width and height are not 0</td></tr><tr><td>invisibility_of_element_located</td><td>invisibility</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether a single element corresponding to xpath appears in the dom structure within the wait time, and whether its width and height are both 0</td></tr><tr><td>frame_to_be_available_and_switch_to_it</td><td>None</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether the frame corresponding to xpath can be cut in within the wait time</td></tr><tr><td>element_to_be_clickable</td><td>clickable</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether a single element corresponding to xpath can be clicked within the wait time</td></tr><tr><td>element_located_to_be_selected</td><td>selected</td><td><p>xpath: str,</p><p>wait: float = 1</p></td><td>Determine whether a single element corresponding to xpath can be selected within the wait time</td></tr><tr><td>text_to_be_present_in_element</td><td>None</td><td><p>xpath: str,</p><p>text: str,</p><p>wait: float = 1</p></td><td>Determine whether a single element corresponding to xpath can contain text content within the wait time</td></tr><tr><td>text_to_be_present_in_element_value</td><td>None</td><td><p>xpath: str,</p><p>value: str,</p><p>wait: float = 1</p></td><td>Determine whether the value text content can appear within the wait time in the value of a single element corresponding to xpath</td></tr><tr><td>alert_is_present</td><td>None</td><td>wait: float = 1</td><td>Determine if there is an alert pop-up</td></tr></tbody></table>

### 'fail\_script' keyword

If the condition contains the keyword 'fail script', the script will be executed after the condition fails

```json
{
    "check": {
        "condition": "presence",
        "xpath": "//*[@id=\"main-metro\"]/ul/li[3]/a[3]",
        "fail_script": [{
            "method": "log",
            "msg": "[fail] login failed"
        }]
    }
}
```

### Logical inversion

The use of the \_not-{your condition}\_\_ instruction can negate the condition result

```json
{
    "check": {
        "condition": "__not-presence__",
        "xpath": "//*[@id=\"main-metro\"]/ul/li[3]/a[3]",
        "fail_script": [{
            "method": "log",
            "msg": "[fail] login failed"
        }]
    }
}
```

### Add your own conditions

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

---
description: Crawlipt includes some built-in actions for better interaction with web pages. At the same time, you can also add your own action methods for expansion.
---

# Action

### 内置的action方法

All script methods (or aliases) are automatically mapped to the execution function, and all parameters correspond one-to-one. All WebElement elements are located through xpath.

| 方法                | 别名                  | 参数                                                                            | 返回值  | 备注                                           |
| ----------------- | ------------------- | ----------------------------------------------------------------------------- | ---- | -------------------------------------------- |
| click             | None                | xpath : str                                                                   | None | 点击某个可点击的按钮                                   |
| clickMulti        | click.multi         | <p>xpath : str</p><p>cnt : str</p>                                            | None | 对某个可点击的按钮点击多次                                |
| clickByJs         | click.js            | xpath : str                                                                   | None | 通过js去点击某个按钮，这种方式可以避开遮罩层影响。但在某些禁用外部js的网站可能会失效 |
| clickAll          | click.all           | xpath: str                                                                    | None | 点击所有可点击的选中元素                                 |
| clickAllByJs      | click.all.js        | xpath: str                                                                    | None | 通过js点击所有可点击的选中元素                             |
| enter             | None                | xpath : str                                                                   | None | 在输入框键入回车                                     |
| input             | None                | <p>xpath : str</p><p>text : str</p>                                           | None | 在输入框输入内容                                     |
| switchLastTab     | switch.tab.last     | None                                                                          | None | 切换到最后一个窗口                                    |
| switchTab         | switch.tab          | index : int                                                                   | None | 切换到第index个窗口                                 |
| switchToFrame     | switch.frame        | xpath : str                                                                   | None | 进入到某个frame中                                  |
| switchOutFrame    | switch.frame.out    | None                                                                          | None | 退出frame                                      |
| searchRedirect    | redirect.search     | <p>url : str</p><p>keyword : str</p>                                          | None | 使用keyword替换链接中的%s进行重定向                       |
| redirect          | None                | url : str                                                                     | None | 重定向                                          |
| redirectNewTab    | redirect.new        | url : str                                                                     | None | 重定向到新窗口                                      |
| selectByText      | select.text         | <p>xpath : str</p><p>text : str</p>                                           | None | 通过文本对下拉选择器选择                                 |
| selectByValue     | select.value        | <p>xpath : str</p><p>value : str</p>                                          | None | 通过值对下拉选择器选择                                  |
| selectByIndex     | select.index        | <p>xpath : str</p><p>index : int</p>                                          | None | 通过index索引对下拉选择器选择                            |
| slide             | None                | <p>xpath : str</p><p>position : list-list([x,y])</p>                          | None | 按住某个对象，滑动到相对于这个对象的(x,y)坐标                    |
| scrollByJs        | scroll.js           | height: str \| int                                                            | None | 通过执行js代码来实现滚动height高度（为负数则向上滚动）              |
| scrollToBottom    | scroll.bottom       | None                                                                          | None | 通过js直接滚动到底部                                  |
| scrollToTop       | scroll.top         | None                                                                          | None | 通过js直接滚动到顶部 
| scrollBySpace     | scroll.space        | <p>cnt: str | int, </p><p>frequency: int = 0.1</p>                            | None | 使用按空格按键来实现滚动                                 |                                 |
| scrollUpByArrow   | scroll.arrow.up   | cnt: str \| int, frequency: float = 0.1                                       | None | 通过上箭头按键实现向上滚动                                |
| scrollDownByArrow | scroll.arrow.down | cnt: str \| int, frequency: float = 0.1                                       | None | 通过下箭头按键实现向下滚动                                |
| alert             | None                | <p>operation: str  option in ["dismiss", "accept"],  </p><p>text: str = "</p> | None | 操作浏览器弹出的alert，并返回alert的内容                    |
| getInnerText      | get.innerText       | xpath : str                                                                   | str  | 获取元素的内部文本，如果元素不可见将获取不到                       |
| getTextContent    | get.textContent     | xpath : str                                                                   | str  | 获取元素的内部文本                                    |
| getAttribute      | get.attribute       | <p>xpath : str</p><p>name : str</p>                                           | str  | 获取元素的某个属性                                    |
| close             | window.close        | None                                                                          | None | 关闭当前窗口                                       |
| back              | window.back         | None                                                                          | None | 在浏览器历史记录中后退一步                                |
| forward           | window.forward      | None                                                                          | None | 在浏览器历史记录中前进一步                                |
| url               | window.url          | None                                                                          | str  | 获取当前窗口的url，并返回                               |
| clear             | window.clear        | None                                                                          | None | 清空所有操作状态                                     |
| html | window.html | None             | str | 返回当前driver的page_source                                |
| log               | None                | msg: Any                                                                      | None | 在终端打印msg信息                                   |
| interval          | None                | num: str \| int                                                               | None | 显式等待num秒时间                                   |
| intervalRandom    | interval.random     | num: str \| int                                                               | None | 显示等待\[num/2, num]秒时间                         |
| execute    | None     | js: str                                                               | Any | 执行js code                         |

### 添加你自己的action

Before adding your own action method, it is recommended that you first learn the basic usage of selenium

{% embed url="https://www.selenium.dev/" %}

Refer to the following example to add your own action

```python
import crawlipt as cpt
from selenium.webdriver.remote.webdriver import WebDriver
"""
(1) Must be a callable function or static method within a class
(2) The check annotation must be used to exclude the syntax check of the driver, otherwise an exception will be thrown during the syntax check phase
(3) All parameters must indicate the type, otherwise they cannot pass the syntax check
(4) All parameters must be of the underlying type in Python
(5) The function return value must be specified. If there is no return value, return None (->None)
(6) Driver is a fixed variable, which means it must include the parameter (driver: WebDriver)
(7) The parameters of the action method cannot contain keywords such as if, check, loop, etc., otherwise they will not take effect
"""
@cpt.check(exclude="driver")  
def myAction(driver: WebDriver, **args) -> None:
    """
    your doc
    :param driver: selenium webdriver
    :param **args: your args
    """
    # write your code


# Add the script as follows
cpt.Script.add_action(myAction)
```

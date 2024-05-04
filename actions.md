---
description: 本框架包含了一些内置的行为，以便你更好地与网页进行交互。同时你也可以添加自己的行为方法，进行扩展。
---

# 🐻 行为

### 内置的行为方法

所有的脚本方法会自动映射到执行函数，所有的参数都是一一对应的，所有的WebElement元素均通过xpath进行定位。

| 方法             | 参数                                                   | 返回值  | 备注                                           |
| -------------- | ---------------------------------------------------- | ---- | -------------------------------------------- |
| click          | xpath : str                                          | None | 点击某个可点击的按钮                                   |
| clickMulti     | <p>xpath : str</p><p>cnt : str</p>                   | None | 对某个可点击的按钮点击多次                                |
| clickByJs      | xpath : str                                          | None | 通过js去点击某个按钮，这种方式可以避开遮罩层影响。但在某些禁用外部js的网站可能会失效 |
| enter          | xpath : str                                          | None | 在输入框键入回车                                     |
| input          | <p>xpath : str</p><p>text : str</p>                  | None | 在输入框输入内容                                     |
| switchLastTab  | None                                                 | None | 切换到最后一个窗口                                    |
| switchTab      | index : int                                          | None | 切换到第index个窗口                                 |
| switchToframe  | xpath : str                                          | None | 进入到某个frame中                                  |
| switchOutFrame | None                                                 | None | 退出frame                                      |
| searchRedirect | <p>url : str</p><p>keyword : str</p>                 | None | 使用keyword替换链接中的%s进行重定向                       |
| redirect       | url : str                                            | None | 重定向                                          |
| redirectNewTab | url : str                                            | None | 重定向到新窗口                                      |
| selectByText   | <p>xpath : str</p><p>text : str</p>                  | None | 通过文本对下拉选择器选择                                 |
| selectByValue  | <p>xpath : str</p><p>value : str</p>                 | None | 通过值对下拉选择器选择                                  |
| selectByIndex  | <p>xpath : str</p><p>index : int</p>                 | None | 通过index索引对下拉选择器选择                            |
| slide          | <p>xpath : str</p><p>position : list-list([x,y])</p> | None | 按住某个对象，滑动到相对于这个对象的(x,y)坐标                    |
| getInnerText   | xpath : str                                          | str  | 获取元素的内部文本，如果元素不可见将获取不到                       |
| getTextContent | xpath : str                                          | str  | 获取元素的内部文本                                    |
| getAttribute   | <p>xpath : str</p><p>name : str</p>                  | str  | 获取元素的某个属性                                    |

### 添加你自己的行为

在你添加自己的行为方法前，建议你先学习一下selenium的基本使用

{% embed url="https://www.selenium.dev/" %}

参考下面的示例来添加你自己的行为

```python
import crawlipt as cpt
from selenium.webdriver.remote.webdriver import WebDriver
"""
（1）必须为一个可调用的函数或者类内的静态方法
（2）必须使用check注解，来排除driver的语法检查，否则在语法检查阶段会抛出异常
（3）所有的参数必须注明类型，否则无法通过语法检查
（4）所有参数必须为python的基础类型
（5）必须注明函数返回值，如果没有返回值，就返回None(-> None)
（6）必须包含(driver: WebDriver)这个参数
"""
@cpt.check(exclude="driver")  
def crackCaptcha(driver: WebDriver, xpath: str) -> str:
    """
    Handling keyboard input events
    :param driver: selenium webdriver
    :param xpath: The xpath path of the captcha
    """
    element = driver.find_element(By.XPATH, xpath)
    pic = element.screenshot_as_png
    ocr = docr.DdddOcr(show_ad=False)
    res = ocr.classification(pic)
    return res

# 按照如下方式添加脚本
cpt.Script.add_action(crackCaptcha)
```

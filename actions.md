---
description: Drive your selenium's webdriver to handle some web page interaction tasks
---

# 🐻 Actions

| methods        | parms                                                                                                                                                             | return |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| click          | xpath : str– Click on the xpath path of the button                                                                                                                | None   |
| clickMulti     | <p>xpath : str– click on the xpath path of the button </p><p>cnt : str | int– click count of the button </p><p>frequency : int– click frequency of the button</p> | None   |
| enter          | xpath : str– The xpath path of the input box                                                                                                                      | None   |
| input          | <p>xpath : str– The xpath path of the input box </p><p>text : str– text needs to be passed in</p>                                                                 | None   |
| switchLastTab  | None                                                                                                                                                              | None   |
| switchTab      | index : int – The index handle                                                                                                                                    | None   |
| switchToframe  | xpath : str– The xpath of frame                                                                                                                                   | None   |
| switchOutFrame | None                                                                                                                                                              | None   |
| searchRedirect | <p>url : str– Link containing %s</p><p>keyword : str– keyword needs to be passed in</p>                                                                           | None   |
| redirect       | url : str– Links that require redirection                                                                                                                         | None   |
| selectByText   | <p>xpath : str– the xpath path of the select element </p><p>text : str– the text of selecting</p>                                                                 | None   |
| selectByValue  | <p>xpath : str– the xpath path of the select element </p><p>value : str– the value of selecting</p>                                                               | None   |
| selectByIndex  | <p>xpath : str– the xpath path of the select element </p><p>index : int – the index of selecting</p>                                                              | None   |
| slide          | <p>xpath : str– The element to be slid </p><p>position : list– The x, y position, list([x,y])</p>                                                                 | None   |
| getInnerText   | xpath : str– The xpath path of the element                                                                                                                        | str    |
| getTextContent | xpath : str– The xpath path of the element                                                                                                                        | str    |
| getAttribute   | <p>xpath : str– The xpath path of the element </p><p>name : str– The name of the attribute</p>                                                                    | str    |

### Add your own action

You can add your own actions to the script, please refer to the following example.

```python
"""
This is a parameter check annotation. 
If it is added, the script will perform 
a parameter check on the current action 
before execution, and you can also ignore it. 
The parm of exclude means you will exclude this 
parameter check.
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

# the parm must be a callable function
cpt.Script.add_action(crackCaptcha)
```

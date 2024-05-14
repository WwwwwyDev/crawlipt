---
description: >-
  Crawlipt includes some built-in actions for better interaction with web pages.
  At the same time, you can also add your own action methods for expansion.
---

# Action

### Built-in action methods

All script methods (or aliases) are automatically mapped to the execution function, and all parameters correspond one-to-one. All WebElement elements are located through xpath.

| method            | alias             | params                                                                     | return                                 | notes                                                                                                                                                     |
| ----------------- | ----------------- | -------------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| click             | None              | xpath : str                                                                | None                                   | Click on a clickable button                                                                                                                               |
| clickMulti        | click.multi       | <p>xpath : str</p><p>cnt : str</p>                                         | None                                   | Click on a clickable button multiple times                                                                                                                |
| clickByJs         | click.js          | xpath : str                                                                | None                                   | Clicking a button through JavaScript can avoid the influence of mask layers. But in some websites that disable external JavaScript, it may become invalid |
| clickAll          | click.all         | xpath: str                                                                 | None                                   | Click on all clickable selected elements                                                                                                                  |
| clickAllByJs      | click.all.js      | xpath: str                                                                 | None                                   | Click on all clickable selected elements through JavaScript                                                                                               |
| enter             | None              | xpath : str                                                                | None                                   | Type enter in the input box                                                                                                                               |
| input             | None              | <p>xpath : str</p><p>text : str</p>                                        | None                                   | Enter content in the input box                                                                                                                            |
| switchLastTab     | switch.tab.last   | None                                                                       | None                                   | Switch to the last window                                                                                                                                 |
| switchTab         | switch.tab        | index : int                                                                | None                                   | Switch to the index window                                                                                                                                |
| switchToFrame     | switch.frame      | xpath : str                                                                | None                                   | Entering a certain frame                                                                                                                                  |
| switchOutFrame    | switch.frame.out  | None                                                                       | None                                   | Exit frame                                                                                                                                                |
| searchRedirect    | redirect.search   | <p>url : str</p><p>keyword : str</p>                                       | None                                   | Replace% s in the link with keyword for redirection                                                                                                       |
| redirect          | None              | url : str                                                                  | None                                   | Redirect to URL website                                                                                                                                   |
| redirectNewTab    | redirect.new      | url : str                                                                  | None                                   | Redirect to a new window                                                                                                                                  |
| selectByText      | select.text       | <p>xpath : str</p><p>text : str</p>                                        | None                                   | Select through text on dropdown selectors                                                                                                                 |
| selectByValue     | select.value      | <p>xpath : str</p><p>value : str</p>                                       | None                                   | Select through a value pair dropdown selector                                                                                                             |
| selectByIndex     | select.index      | <p>xpath : str</p><p>index : int</p>                                       | None                                   | Selecting dropdown selectors through index indexing                                                                                                       |
| slide             | None              | <p>xpath : str</p><p>position : list-list([x,y])</p>                       | None                                   | Selecting dropdown selectors through index indexing                                                                                                       |
| scrollByJs        | scroll.js         | height: str \| int                                                         | None                                   | Implement scrolling height by executing JavaScript code (scroll up if negative)                                                                           |
| scrollToBottom    | scroll.bottom     | None                                                                       | None                                   | Scroll directly to the bottom through JavaScript                                                                                                          |
| scrollToTop       | scroll.top        | None                                                                       | None                                   | Scroll directly to the top through JavaScript                                                                                                             |
| scrollBySpace     | scroll.space      | cnt: str                                                                   | <p>int,</p><p>frequency: int = 0.1</p> | Scroll down through spaces                                                                                                                                |
| scrollUpByArrow   | scroll.arrow.up   | cnt: str \| int, frequency: float = 0.1                                    | None                                   | Use the up arrow button to scroll up                                                                                                                      |
| scrollDownByArrow | scroll.arrow.down | cnt: str \| int, frequency: float = 0.1                                    | None                                   | Use the down arrow button to scroll down                                                                                                                  |
| alert             | None              | <p>operation: str option in ["dismiss", "accept"],</p><p>text: str = "</p> | None                                   | Operate the pop-up alert in the browser and return the content of the alert                                                                               |
| getInnerText      | get.innerText     | xpath : str                                                                | str                                    | Get the internal text of the element, if the element is not visible, it will not be obtained                                                              |
| getTextContent    | get.textContent   | xpath : str                                                                | str                                    | Get the internal text of the element                                                                                                                      |
| getAttribute      | get.attribute     | <p>xpath : str</p><p>name : str</p>                                        | str                                    | Get a certain attribute of an element                                                                                                                     |
| close             | window.close      | None                                                                       | None                                   | Close the current window                                                                                                                                  |
| back              | window.back       | None                                                                       | None                                   | Step back in browser history                                                                                                                              |
| forward           | window.forward    | None                                                                       | None                                   | Take a step forward in browser history                                                                                                                    |
| url               | window.url        | None                                                                       | str                                    | Get the URL of the current window and return it                                                                                                           |
| clear             | window.clear      | None                                                                       | None                                   | Clear all operation states                                                                                                                                |
| html              | window.html       | None                                                                       | str                                    | Return the page\_source of the current driver                                                                                                             |
| log               | None              | msg: Any                                                                   | None                                   | Print msg information on the terminal                                                                                                                     |
| interval          | None              | num: str \| int                                                            | None                                   | Explicitly wait for num seconds                                                                                                                           |
| intervalRandom    | interval.random   | num: str \| int                                                            | None                                   | Explicitly wait for \[num/2, num] seconds                                                                                                                 |
| execute           | None              | js: str                                                                    | Any                                    | Execute JavaScript code                                                                                                                                   |

### Add your own action

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

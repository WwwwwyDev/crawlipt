---
layout:
  title:
    visible: false
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Overview

[![crawlipt](https://s2.loli.net/2024/05/10/PCcpwynVMmURjBv.png)](https://github.com/WwwwwyDev/crawlipt)

## crawlipt

Using string scripts to drive selenium

[![pypi](https://img.shields.io/pypi/v/crawlipt) ](https://pypi.python.org/pypi/crawlipt)![python](https://img.shields.io/badge/python-3.10.0+-blue) [![GitHub stars](https://img.shields.io/github/stars/WwwwwyDev/crawlipt)](https://github.com/WwwwwyDev/crawlipt/stargazers)

{% embed url="https://github.com/WwwwwyDev/crawlipt" %}

{% embed url="https://gitee.com/wu_wen_yi/crawlipt" %}

### introduce

In Python, you can use this framework to drive selenium's webdriver, with scripts in JSON format for better cross language operations and textual storage on physical storage.

### install

You can use pip or pip3 to install crawlipt

`pip install crawlipt` 或 `pip3 install crawlipt`

If you have already installed crawlipt, you may need to update to the latest version

`pip install --upgrade crawlipt`

### quickly start

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt

def getDriver(is_headless=False):
    option = wd.ChromeOptions()
    arguments = [
        "no-sandbox",
        "--disable-extensions",
        '--disable-gpu',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
        "window-size=1920x3000",
        "start-maximized",
        'cache-control="max-age=0"'
        "disable-blink-features=AutomationControlled"
    ]
    for argument in arguments:
        option.add_argument(argument)
    if is_headless:
        option.add_argument("--headless")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })
    return webdriver

if __name__ == '__main__':
    webdriver = getDriver()
    # Define scripts that comply with script specifications
    # You can also serialize dictionaries into JSON strings
    script = {
        "method": "redirect",
        "url": "https://www.baidu.com/",
        "next": {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "keyword": "selenium",
            "next": {
                "method": "click",
                "xpath": "//*[@id=\"su\"]"
            }
        }
    }
    # Execute the script, which can directly pass in the JSON string and will automatically parse and execute it
    cpt.Script(script, interval=2)(webdriver)
```

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

# 概述

[![crawlipt](https://s2.loli.net/2024/05/10/PCcpwynVMmURjBv.png)](https://github.com/WwwwwyDev/crawlipt)

## crawlipt

使用字符串脚本驱动selenium

[![pypi](https://img.shields.io/pypi/v/crawlipt) ](https://pypi.python.org/pypi/crawlipt)![python](https://img.shields.io/badge/python-3.10.0+-blue) [![GitHub stars](https://img.shields.io/github/stars/WwwwwyDev/crawlipt)](https://github.com/WwwwwyDev/crawlipt/stargazers)

{% embed url="https://github.com/WwwwwyDev/crawlipt" %}

{% embed url="https://gitee.com/wu_wen_yi/crawlipt" %}

### 介绍

在python中，你可以使用本框架去驱动selenium的webdriver，脚本使用json格式，以便你更好地跨语言操作以及以文本方式存储在物理介质中。

### 安装

你可以使用 pip 或者 pip3 来安装crawlipt

`pip install crawlipt` 或 `pip3 install crawlipt`

如果你已经安装了crawlipt，可能需要更新到最新版本

`pip install --upgrade crawlipt`

### 快速开始

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
    # 定义脚本，需要符合脚本规范
    # 你也可以字典序列化成json字符串
    script = {
        "method": "redirect",
        "url": "https://www.baidu.com/",
        "next": {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "keyword": "和泉雾纱",
            "next": {
                "method": "click",
                "xpath": "//*[@id=\"su\"]"
            }
        }
    }
    # 执行脚本，可以直接传入json字符串，会自动解析并执行
    cpt.Script(script, interval=2)(webdriver)
```

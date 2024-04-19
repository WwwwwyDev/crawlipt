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

# 🐻 Overview

[![crawlist](https://s2.loli.net/2024/04/19/1T7sZdrjbEfci8W.png)](https://github.com/WwwwwyDev/crawlipt)

## crawlipt

The script for selenium in python

[![pypi](https://img.shields.io/pypi/v/crawlipt) ](https://pypi.python.org/pypi/crawlipt)![python](https://img.shields.io/badge/python-3.10.0+-blue) [![GitHub stars](https://img.shields.io/github/stars/WwwwwyDev/crawlipt)](https://github.com/WwwwwyDev/crawlipt/stargazers)\


### introduction

You can use Crawlipt to driver the selenium by script in python.The script adopts JSON format for better cross language operations and physical storage.

### installing

You can use pip or pip3 to install the crawlist\
`pip install crawlipt` or `pip3 install crawlipt`

### quickly start

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt
option = wd.ChromeOptions()
option.add_argument("start-maximized")
option.add_argument("window-size=1920x3000")
agent = 'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
option.add_argument(agent)
webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)

# Define scripts
# You can also deserialize JSON strings into a dictionary
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
# Execute script
cpt.Script(script, interval=2)(webdriver)

```

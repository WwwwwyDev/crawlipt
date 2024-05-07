<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://github.com/WwwwwyDev/crawlipt"><img src="https://s2.loli.net/2024/04/19/1T7sZdrjbEfci8W.png" alt="crawlist" style="width:254px; height:208px" ></a>
</p>

<div align="center">

# crawlipt

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
The script for selenium in python
<!-- prettier-ignore-end -->

<p align="center">
  <a href="https://pypi.python.org/pypi/crawlipt">
    <img src="https://img.shields.io/pypi/v/crawlipt" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.10.0+-blue" alt="python">
  <a href="https://github.com/WwwwwyDev/crawlipt/stargazers"><img src="https://img.shields.io/github/stars/WwwwwyDev/crawlipt" alt="GitHub stars"style="max-width: 100%;">
  </a>
  <br/>
</p>
</div>


## introduction

You can use Crawlipt to driver the selenium by script in python.The script adopts JSON format for better cross language operations and physical storage.

## installing
You can use pip or pip3 to install the crawlipt

`pip install crawlipt` or `pip3 install crawlipt`

If you have already installed crawlipt, you may need to update to the latest version

`pip install --upgrade crawlipt`

## quickly start
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


## Documenting
If you are interested and would like to see more detailed documentation, please click on the link below.

[中文](https://wwydev.gitbook.io/crawlipt-zh "中文文档")|[English](https://wwydev.gitbook.io/crawlipt "English Document")

## Contributing
Please submit pull requests to the develop branch
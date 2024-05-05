---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# 🐻‍❄️ 示例

### 需要的依赖

在你测试这些示例前，你需要安装一些依赖包

```sh
pip install webdriver-manager
pip install ddddocr
```

{% embed url="https://github.com/SergeyPirogov/webdriver_manager" %}

{% embed url="https://github.com/sml2h3/ddddocr" %}

### 配置selenium的webdriver

在使用脚本前，你需要配置好自己的webdrvier。

```python
import random
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt
import ddddocr as docr

def get_driver(is_headless=False):
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
```

### 百度搜索示例

在百度中搜索“百度贴吧”

```python
webdriver = get_driver()
script = {
    "method": "redirect",
    "url": "https://www.baidu.com/",
    "next": {
        "method": "input",
        "xpath": "//*[@id=\"kw\"]",
        "text": "百度贴吧",
        "next": {
            "method": "click",
            "xpath": "//*[@id=\"su\"]"
        }
    }
}
cpt.Script(script, interval=0.1)(webdriver)
webdriver.quit()
```

### 使用百度翻译进行翻译

使用百度翻译，并返回翻译结果

```python
webdriver = get_driver(is_headless=True)
step = [{
    "method": "redirect",
    "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
}, {
    "method": "input",
    "xpath": "//*[@id=\"editor-text\"]/div[1]/div[1]/div/div/div/div",
    "text": "你好，世界",
}, {
    "method": "getInnerText",
    "xpath": "//*[@id=\"trans-selection\"]/div/span",
}]
script = cpt.Script.generate(step)
result = cpt.Script(script, interval=0.1)(webdriver)
print(result)
webdriver.quit()
```

### 自动做题

```python
webdriver = get_driver()
step = [{
    "method": "redirect",
    "url": "https://www.psy525.cn/ceshi/84307.html",
}, {
    "method": "click",
    "xpath": "//*[@id=\"fun\"]/a"
}]
for i in range(90):
    index = random.randint(1, 5)
    step.append({
        "method": "click",
        "xpath": f"//*[@id=\"question_{i + 1}\"]/fieldset/ul/li[{index}]"
    })

scripts = cpt.Script.generate(step)
json = cpt.Script.generate_json(scripts)
print(json)
cpt.Script(scripts, interval=1)(webdriver)
webdriver.quit()
```

### \_\_ PRE RETURN\_\_的使用

```python
webdriver = get_driver()
step = [{
    "method": "redirect",
    "url": "https://artsandculture.google.com/",
},{
    "method": "click",
    "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[1]/div[3]/div[2]/span/span",
},{
    "method": "getInnerText",
    "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a"
},{
    "method": "input",
    "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
    "text": "__PRE_RETURN__",
},{
    "method": "enter",
    "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
}]
scripts = cpt.Script.generate(step)
cpt.Script(scripts, interval=1)(webdriver)
webdriver.quit()
```

### 破解验证码

添加自己的action方法使用ddddocr去破解验证码，并返回破解结果，传递到下一个action方法

```python
webdriver = get_driver()
@cpt.check(exclude="driver")
@cpt.alias("captcha")
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

cpt.Script.add_action(crackCaptcha)
step = [{
    "method": "redirect",
    "url": "http://www.shuhai.com/login",
},{
    "method": "input",
    "xpath": "//*[@id=\"login_form\"]/div[2]/div[1]/div[2]/input",
    "text": "username",
},{
    "method": "input",
    "xpath": "//*[@id=\"login_form\"]/div[2]/div[2]/div[2]/input",
    "text": "password",
},{
    "method": "crackCaptcha",  # or alias: "method": "captcha"
    "xpath": "//*[@id=\"checkcode2\"]",
},{
    "method": "input",
    "xpath": "//*[@id=\"login_form\"]/div[2]/div[3]/div[2]/input",
    "text" : "__PRE_RETURN__"
},{
    "method": "click",
    "xpath": "//*[@id=\"dosubmit\"]",
}]
scripts = cpt.Script.generate(step)
cpt.Script(scripts, interval=3)(webdriver)
webdriver.quit()
```

### if条件判断

通过if判断是否需要在输入框进行输入

```python
webdriver = get_driver()
step = [{
    "method": "redirect",
    "url": "https://www.baidu.com/",
}, {
    "method": "input",
    "xpath": "//*[@id=\"kw\"]",
    "text": "your search text",
    "if": {
        "condition": "presence",
        "xpath": "//*[@id=\"su\"]"
    }
}, {
    "method": "input",
    "xpath": "//*[@id=\"kw\"]",
    "text": "your search text",
}]
cpt.Script(step, interval=3)
```

### 计数器多层嵌套循环计算

添加自己的condition方法进行加减计数，并返回最后的结果

```python
webdriver = get_driver()

@cpt.check(exclude="driver")
@cpt.alias("check")
def checkNum(driver: WebDriver, xpath: str) -> bool:
    """
    your doc
    :param driver: selenium webdriver
    :param xpath: the xpath of element
    """
    element = driver.find_element(By.XPATH, xpath)
    value = int(element.get_attribute("value"))
    if value > 10:
        return False
    else:
        return True

cpt.Script.add_condition(checkNum)

step = [{
    "method": "redirect",
    "url": "https://www.bchrt.com/tools/click-counter/",
}, {
    "loop": {
        "while": {
            "condition": "checkNum",  # or alias: "condition": "check",
            "xpath": "//*[@id=\"count\"]"
        },
        "script": [{
            "loop": {
                "cnt": 5,
                "script": {
                    "method": "click",
                    "xpath": "//*[@id=\"addbtn\"]",
                },
            }
        },
            {
                "method": "click",
                "xpath": "//*[@id=\"subbtn\"]",
            }
        ]
    }
}, {
    "method": "getAttribute",
    "xpath": "//*[@id=\"count\"]",
    "name": "value"
}]
json_str = cpt.Script.generate_json(step)
res = cpt.Script(json_str)(webdriver)
print(res)
webdriver.quit()
```

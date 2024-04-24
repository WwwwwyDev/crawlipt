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

# 🐻‍❄️ Demo

### Definition of driver

Before using the script, you need to define your own webdriver.

```python
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
```

### demo1

Search in baidu

```python
webdriver = getDriver()
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

### demo2

Translate using Baidu Translate

```python
webdriver = getDriver(is_headless=True)
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

### demo3

Automatic problem-solving

```python
webdriver = getDriver()
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

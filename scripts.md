---
description: >-
  The script is defined using JSON, which requires deserializing the JSON string
  into Python's dict and then parsing it.
---

# 🐻 Scripts

### Conversion method

```python
import crawlipt as cpt

# the origin script you wrote
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
script_json = cpt.Script.dict2json(script)  # Convert it to a string and store it in a database or other medium
script_dict = cpt.Script.json2dict(script_json)  # Load the json as a dict
```

### Execute script

Scripts can map all action methods

```python
webdriver = getDriver()
# Pass in a JSON format script, which can be a Python dict or a JSON string
loader = cpt.Script(script, interval=0.1)
# To execute the script, you need to pass in a selenium Webdriver object
loader.process(webdriver) 
# loader(webdriver) 
webdriver.quit()
```

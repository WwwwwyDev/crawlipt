---
description: >-
  The script is defined using JSON, which requires deserializing the JSON string
  into Python's dict and then parsing it.
---

# 🐻 scripts

### Conversion method

<pre class="language-python"><code class="lang-python"><strong>import crawlipt as cpt
</strong><strong>
</strong><strong># the origin script you wrote
</strong><strong>script = {
</strong>    "method": "redirect",
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
</code></pre>

### Execute script

<pre class="language-python"><code class="lang-python">webdriver = getDriver()
<strong># Pass in a JSON format script, which can be a Python dict or a JSON string
</strong>loader = cpt.Script(script, interval=0.1)
# To execute the script, you need to pass in a selenium Webdriver object
loader.process(webdriver) 
# loader(webdriver) 
webdriver.quit()
</code></pre>

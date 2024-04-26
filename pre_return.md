---
description: >-
  If the previous action has a return value, the next action needs to receive
  this return value through the keyword of "__PRE_RETURN__".
---

# 🐻 Pre\_Return

### Return value in the middle

<pre class="language-python"><code class="lang-python"><strong>script = {
</strong>	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
		"text": "__PRE_RETURN__" # The text parameter of the input action will be the return value of the previous action
	}
}
</code></pre>

### Return value at the end

```python
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
result = cpt.Script(script, interval=0.1)(webdriver) # You can use a variable to accept it
```

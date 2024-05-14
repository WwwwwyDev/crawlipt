---
description: >-
  If the preceding action has a return value, the following action can receive this return value through the identifier "_PRE-RETURN__", and the types of the return and receiver must be the same. Note: The identifier "_ PRE-RETURN__" can only be used for return value transfer between actions.
---

# Pre-Return

### action在脚本中的返回值

```python
script = {
	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
		"text": "__PRE_RETURN__"  # The value of the text parameter will be the return value of the previous action
	}
}
```

### 在脚本最后的返回值

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
result = cpt.Script(script, interval=0.1)(webdriver)  # You can use a variable to receive
```

### 返回值延迟传播

If an action has a return value and all n actions below have a return value of None, the return value of that action will propagate all the way to the n actions below, meaning that all n actions below can receive the return value. Until an action with a return value appears, the propagation will be terminated.

```python
script = {
	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
		"text": "__PRE_RETURN__"
		"next": {
			"method": "input",
			"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
			"text": "__PRE_RETURN__"
		}
	}
}
```


---
description: 如果前面的action有一个返回值，则后面的action可以通过关键词"__PRE_RETURN__"来接收这个返回值，返回方和接收方的类型必须相同。
---

# Pre-Return

### 在脚本中的返回值

```python
script = {
	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
		"text": "__PRE_RETURN__" # text参数的值将是前面action的返回值
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
result = cpt.Script(script, interval=0.1)(webdriver) # 你可以使用一个变量去接收
```

### 返回值延迟传播

如果某个action有返回值，下面n个action返回值均为None，则该action的返回值，会一直传播到下面n个action，即下面的n个action均能接收到该返回值。直到有一个有返回值action出现，会终止该传播。

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

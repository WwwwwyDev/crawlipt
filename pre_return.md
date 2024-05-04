---
description: 如果前面的行为有一个返回值，则后面的行为可以通过关键字"__PRE_RETURN__"来接收这个返回值，返回方和接收方的类型必须相同。
---

# 🐻 返回值

### 在脚本中的返回值

```python
script = {
	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
		"text": "__PRE_RETURN__" # text参数的值将是前面行为的返回值
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

如果某个行为有返回值，下面n个行为返回值均为None，则该行为的返回值，会一直传播到下面n个行为，即下面的n个行为均能接收到该返回值。直到有一个有返回值行为出现，会终止该传播。

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

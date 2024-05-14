---
description: 'The identifier "_ PRE-RETURN__" cannot skip accepting parameters and cannot be passed to the condition. To address this issue, the return_flag is introduced.'
---

# Return\_flag

### return\_flag关键词

如果你后面的action方法或condition判断需要接收前面的某个action方法或condition判断的返回值，但是中间有action方法返回了返回值，导致无法接受，则需要配合return\_flag关键词以及标识符"\_\_rf-{your return\_flag}\_\_"来接受

```json
script = {
	"method": "getInnerText",
	"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a",
	"return_flag": "text1"
	"next": {
		"method": "getInnerText",
		"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a[2]",
		"if": {
	            "condition": "is_over_evaluation",
	            "xpath": "__rf-text1__",
		    "return_flag": "is_success"
	        },
		"next": {
			"method": "input",
			"xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
			"text": "__rf-text1__"
			"is_inpt": "__rf-is_success__"
		}
	}
}
```

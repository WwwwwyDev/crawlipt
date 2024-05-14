---
description: >-
  The identifier "_ PRE-RETURN__" cannot skip accepting parameters and cannot be
  passed to the condition. To address this issue, the return_flag is introduced.
---

# Return\_flag

### 'return\_flag' keyword

If your subsequent action method or condition judgment needs to receive the return value of a previous action method or condition judgment, but there is an action method in the middle that returns the return value, which cannot be accepted, then you need to cooperate with the return\_flag keyword and identifier "\_\_ rf - {your return\_flag} \_\_" to accept it.

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

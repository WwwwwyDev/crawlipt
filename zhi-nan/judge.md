---
description: >-
  Crawlipt provides two keywords, if and check, combined with the condition
  method to make logical judgments before executing the action method.
---

# Judge

### 'If' keyword

Add the if keyword in the same layer of the action method, and the corresponding judgment logic will be mapped to the corresponding condition method (or alias).

If the if condition does not hold, the current action method will be skipped to execute the next action method, and the if keyword must appear simultaneously with the method keyword.

```json
{
    "method": "input",
    "xpath": "//*[@id=\"kw\"]",
    "text": "your search text",
    "if": {
        "condition": "presence",
        "xpath": "//*[@id=\"su\"]"
    }
}
```

### 'check' keyword

Unlike the if keyword, the check keyword will directly terminate the current process when the conditions are not met

```json
{
    "method": "input",
    "xpath": "//*[@id=\"kw\"]",
    "text": "your search text",
    "check": {
        "condition": "presence",
        "xpath": "//*[@id=\"su\"]"
    }
}

//Equivalent to
{
	"check": {
		"condition": "presence",
		"xpath": "//*[@id=\"su\"]"
	},
	"next": {
		"method": "input",
		"xpath": "//*[@id=\"kw\"]",
		"text": "your search text"
	}
}
```

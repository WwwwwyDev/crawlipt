---
description: crawlipt提供了loop关键词来进行循环
---

# Loop

### loop关键词

When a layer contains the loop keyword, the script will directly enter the script within the loop and loop based on the while or cnt conditions. After the loop terminates, it will skip the current layer and enter the next layer to execute the action method of the next layer.

### loop条件

The loop keyword has two conditions: while and cnt. The while condition can be evaluated in conjunction with the condition method. If the condition method is false, the loop is terminated. The CNT condition is a counter, which means the script will loop CNT times. If both condition and cnt conditions occur simultaneously, both conditions need to be met before the loop can continue.

### loop脚本

The loop script needs to be passed in using script keywords within the loop, supporting JSON, dict, and list types

### loop示例

Note: Loop can be nested multiple times

```json
step = [{
    "method": "redirect",
    "url": "https://www.bchrt.com/tools/click-counter/",
}, {
    "loop": {
        "while": {
            "condition": "checkNum",
            "xpath": "//*[@id=\"count\"]"
        },
        "script": [{
            "loop": {
                "cnt": 5,
                "script": {
                    "method": "click",
                    "xpath": "//*[@id=\"addbtn\"]",
                },
            }
        },
            {
                "method": "click",
                "xpath": "//*[@id=\"subbtn\"]",
            }
        ]
    }
}, {
    "method": "getAttribute",
    "xpath": "//*[@id=\"count\"]",
    "name": "value"
}]
```

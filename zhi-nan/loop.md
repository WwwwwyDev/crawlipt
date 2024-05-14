---
description: crawlipt提供了loop关键词来进行循环
---

# Loop

### loop关键词

当某一层中含有loop关键词，脚本会直接进入loop内的脚本，根据while或者cnt条件进行循环。循环终止后会跳过当前层，进入下一层执行下一层的action方法。

### loop条件

loop关键词有while和cnt两个条件。while条件可以结合condition方法进行判断，如果condition方法为假，则终止循环。cnt条件是一个计数器，意味着脚本将循环cnt次。如果condition和cnt条件同时出现，则需要两个条件同时满足才会继续循环。

### loop脚本

loop的脚本需要在loop内使用script关键词传入，支持json、dict、list类型

### loop示例

注：loop可以多次嵌套

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

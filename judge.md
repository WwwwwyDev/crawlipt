---
description: crawlipt提供了if和check两个关键词结合condition方法来进行action方法执行前的逻辑判断
---

# 🐻 Judge

### if关键词

在action方法同层中添加if关键词，对应的判断逻辑会映射到对应的condition方法（或别名）中。

如果if条件不成立，则会跳过当前的action方法去执行下一个action方法

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

### check关键词

与if关键词不同的是，check关键词会在条件不满足时直接终止当前流程

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
```

---
description: >-
  This chapter introduces the basic use of scripts. The script is defined in
  JSON format and can be easily deserialized in various languages.
---

# Script

### Conversion method

```python
import crawlipt as cpt

# During the writing phase, Python built-in dictionary types can be used for writing
script = { 
    "method": "redirect",
    "url": "https://www.baidu.com/",
    "next": {
        "method": "input",  # Method name
        "xpath": "//*[@id=\"kw\"]", # Method corresponding parameters
        "text": "baidu tieba", # Method corresponding parameters
        "next": { # Next script to execute
            "method": "click",
            "xpath": "//*[@id=\"su\"]"
        }
    }
}
# Convert to a JSON string, which can be stored in a physical medium
script_json = cpt.Script.generate_json(script) 
```

### Execute Script

Scripts can map all action methods

```python
webdriver = getDriver()
# Pass in a pre written script that supports JSON strings, Python dictionaries, and list types
loader = cpt.Script(script, interval=0.1)
# Pass in the webdriver object of your configured selenium for execution
loader.process(webdriver) 
# loader(webdriver) 
# You need to close your webdriver after execution
webdriver.quit()
```

### Introduction to Script initialization parameters

| parameter name          | type                       | introduction                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| script                  | dict \| str \| list        | Pre-written scripts                                                                                                                                                                                                                                                                                                                                                                        |
| global\_script          | dict \| str \| list = None | Global execution script, which will be executed before each execution of any action method. For example, some websites may randomly pop up advertisements, affecting the execution of the following script. Defining this script can determine whether there are advertisements before executing the action method, and if so, perform a series of operations to close the advertisements. |
| interval                | float = 0.5                | The interval between every two execution of the action method                                                                                                                                                                                                                                                                                                                              |
| wait                    | float = 10                 | If the action method contains xpath or CSS parameters, it will automatically implicitly wait for wait seconds until the corresponding element appears in the dom structure.                                                                                                                                                                                                                |
| is\_need\_syntax\_check | bool = True                | Do you need to perform strict script syntax checks before execution? If closed, it will increase the probability of errors during execution.                                                                                                                                                                                                                                               |

### Introduction to Script Executor Parameters

| parameter name                                                         | type                        | introduction                                                                       |
| ---------------------------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------- |
| [webdriver](https://www.selenium.dev/documentation/webdriver/drivers/) | WebDriver                   | The webdriver object of selenium needs to be configured according to the situation |
| [variable](variable.md)                                                | VariableBase \| None = None | The variable value executed this time                                              |
| [store](store.md)                                                      | StoreBase \| None = None    | The memory for this execution                                                      |

### Writing scripts through list step method

Writing scripts using dictionary types may result in nested dictionaries being too deep and difficult to maintain in situations with multiple actions. Writing scripts using a list approach can turn nested processes into serial processes.

```python
step = [{
            "method": "redirect",
            "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"editor-text\"]/div[1]/div[1]/div/div/div/div",
            "text": "Hello, World",
        }, {
            "method": "getInnerText",
            "xpath": "//*[@id=\"trans-selection\"]/div/span",
        }]

# You can use generate to convert the list script into a dictionary script
script_dict = cpt.Script.generate(step)
# You can use generate_JSON to directly convert the list script into a JSON string
script_json = cpt.Script.generate_json(step)
# Executors can also directly execute list scripts
loader = cpt.Script(step, interval=0.1)
loader.process(webdriver) 
```

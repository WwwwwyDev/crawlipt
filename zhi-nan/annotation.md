---
description: Crawlipt provides two decorators, check and alias, to control the action and condition methods
---

# Annotation

### check 装饰器

The check decorator is used to check the parameters during function calls. If the parameters do not match the type during the call, an exception is thrown. Using the check decorator can enhance script checking and avoid errors caused by illegal parameter types during script execution. The exclude parameter means that you will exclude the checks for these parameters. Note: Any type will automatically exclude checks.

```python
import crawlipt as cpt

@cpt.check(exclude=["a","b"])
def A(a:str,b:int,c:float):
    pass
```

### alias 装饰器

The alias decorator can add an alias to the action and condition methods you add, and the script can map to the function through the alias. Replacement rule: If alias is not set, method name mapping will be performed directly. If the method name already exists, it will not be overwritten and the addition will fail; After setting alias, map both method name and alias name. If both method name and alias exist, the method name will not be overwritten, and alias will be overwritten. Try to avoid duplicate names as much as possible.

```python
import crawlipt as cpt

@cpt.alias(name="B")
def A(a:str,b:int,c:float):
    pass
```

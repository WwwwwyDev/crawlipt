import crawlipt.conditions as conditions
import inspect

classes = []
for element in inspect.getmembers(conditions, inspect.isclass):
    if len(element) > 1:
        classes.append(element[1])


class Condition(*classes):
    """
    Crawler Condition class.
    """
    pass

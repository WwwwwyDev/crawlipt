import crawlipt.actions as actions
import inspect

classes = []
for element in inspect.getmembers(actions, inspect.isclass):
    if len(element) > 1:
        classes.append(element[1])


class Action(*classes):
    """
    Crawler Action class.
    """
    pass

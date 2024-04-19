import random
import time
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, ParamTypeError
from crawlipt.action import Action
import json
import copy
from inspect import signature


class ScriptError(Exception):
    def __init__(self, e: Exception, method: str, deep: int):
        self.e = e
        self.method = method
        self.deep = deep

    def __str__(self):
        doc: str = Script.ACTIONS[self.method].__doc__
        info = "----------------------method info--------------------------"
        params = "\ndef " + self.method + " " + signature(Script.ACTIONS[self.method]).__str__()
        error = "[" + self.e.__class__.__name__ + "] " + self.e.__str__() + "\n"
        return "(Deep:%d method:%s) arguments is wrong\n" % (self.deep, self.method) + error + info + params + doc


def get_action_dict():
    all_action = {}
    for parent in Action.__bases__:
        all_action.update(parent.__dict__)
    for key in list(all_action.keys()):
        if key.startswith("__") and key.endswith("__"):
            all_action.pop(key)
    return all_action


class Script:
    ACTIONS = get_action_dict()

    @check
    def __init__(self, script: dict | str, interval: float = 2):
        """
        Script Parser
        :param script: Need a JSON str or dict that conforms to syntax conventions
        :param interval: The direct interval between two consecutive scripts
        """
        if isinstance(script, str):
            self.script = json.loads(script)
        else:
            self.script = script
        Script.check_script(self.script)
        self.interval = interval

    @check
    def process(self, webdriver: WebDriver) -> None:
        """
        process the script
        """
        script = self.script
        pre_return = None
        while script:
            temp = copy.deepcopy(script)
            method = temp.get("method")
            if temp.get("next"):
                temp.pop("next")
            temp.pop("method")
            temp["driver"] = webdriver
            if pre_return is not None:
                for key, value in temp.items():
                    if value == "__PRE_RETURN__":
                        temp[key] = pre_return
            pre_return = Script.ACTIONS[method](**temp)
            script = script.get("next")
            time.sleep(random.uniform(self.interval / 2, self.interval))

    @staticmethod
    @check
    def check_script(script: dict | str) -> None:
        """
        Script syntax check
        """
        deep = 0
        pre_return = None
        while script:
            deep += 1
            temp = copy.deepcopy(script)
            method = temp.get("method")
            if not method:
                raise ScriptError("(Deep %d) Method is missing" % deep)
            if 'next' in temp:
                temp.pop("next")
            temp.pop("method")
            temp["driver"] = None
            if pre_return is not None:
                for key, value in temp.items():
                    if value == "__PRE_RETURN__":
                        annotation = signature(Script.ACTIONS[method]).parameters[key].annotation
                        if pre_return != annotation:
                            msg = f"The pre-return is {pre_return}, But parameter {key} is {annotation}."
                            e = ParamTypeError(msg)
                            raise ScriptError(e, method, deep)
            try:
                pre_return = signature(Script.ACTIONS[method]).return_annotation
                Script.ACTIONS[method](**temp)
            except TypeError as e:
                raise ScriptError(e, method, deep)
            except AssertionError as e:
                raise ScriptError(e, method, deep)
            except ParamTypeError as e:
                raise ScriptError(e, method, deep)
            except Exception:
                pass
            script = script.get("next")

    def __call__(self, webdriver: WebDriver):
        return self.process(webdriver)

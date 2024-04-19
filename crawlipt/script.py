import random
import time
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, ParamTypeError
from crawlipt.action import Action
import json
import copy
from inspect import signature


class ScriptError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


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
        self.check_script()
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

    def check_script(self) -> None:
        """
        Script syntax check
        """
        script = self.script
        deep = 0
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
            try:
                Script.ACTIONS[method](**temp)
            except TypeError as e:
                Script.error(e, method, deep)
            except AssertionError as e:
                Script.error(e, method, deep)
            except ParamTypeError as e:
                Script.error(e, method, deep)
            except Exception:
                pass
            script = script.get("next")

    @staticmethod
    def error(e: Exception, method: str, deep: int) -> None:
        doc: str = Script.ACTIONS[method].__doc__
        info = "----------------------method info--------------------------"
        params = "\ndef " + method + " " + signature(Script.ACTIONS[method]).__str__()
        error = "[" + e.__class__.__name__ + "] " + e.__str__() + "\n"
        raise ScriptError(
            "(Deep:%d method:%s) arguments is wrong\n" % (deep, method) + error + info + params + doc)

    def __call__(self, webdriver: WebDriver):
        return self.process(webdriver)
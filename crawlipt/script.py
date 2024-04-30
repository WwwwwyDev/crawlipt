import random
import time
import json
from inspect import signature
from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from crawlipt.annotation import check, ParamTypeError
from crawlipt.action import Action
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ScriptError(Exception):
    def __init__(self, e: Exception, method: str, deep: str):
        self.e = e
        self.method = method
        self.deep = deep

    def __str__(self):
        info = ""
        params = ""
        doc = ""
        if self.method and self.method in ScriptProcess.ACTIONS.keys():
            params = "\ndef " + self.method + " " + signature(Script.ACTIONS[self.method]).__str__()
            doc = ScriptProcess.ACTIONS[self.method].__doc__
            info = "----------------------method info--------------------------"
        error = "[" + self.e.__class__.__name__ + "] " + self.e.__str__() + "\n"
        return "(Deep:%s method:%s) arguments is wrong\n" % (self.deep, self.method) + error + info + params + doc


def dfs_search(obj):
    for parent in obj.__bases__:
        if parent == object:
            continue
        dfs_search(parent)
        yield parent.__dict__


def get_action_dict():
    all_action = {}
    for element in dfs_search(Action):
        all_action.update(element)
    for key in list(all_action.keys()):
        if key.startswith("__") and key.endswith("__"):
            all_action.pop(key)
    return all_action


class ScriptProcess:
    ACTIONS = get_action_dict()
    POP_KEY = {"method", "next"}

    @staticmethod
    @check
    def syntax_check(script: dict | str, pre_deep: str = "") -> None:
        """
        Script syntax check
        """
        if isinstance(script, str):
            script = ScriptProcess.json2dict(script)
        current_deep = 0
        pre_return = None
        while script and isinstance(script, dict):
            current_deep += 1
            temp_args = {"driver": None}
            loop_temp: dict = script.get("loop")
            if loop_temp:
                cnt = loop_temp.get("cnt")
                if not cnt:
                    msg = "(Deep %s) loop must set the param of cnt" % (pre_deep + str(current_deep))
                    raise ScriptError(ParamTypeError(msg), "", pre_deep + str(current_deep))
                loop_script = loop_temp.get("script")
                ScriptProcess.syntax_check(loop_script, pre_deep=str(current_deep) + "->")
                script = script.get("next")
                continue
            method = script.get("method")
            if not method:
                msg = "(Deep %s) Method is missing" % (pre_deep + str(current_deep))
                raise ScriptError(ParamTypeError(msg), "", pre_deep + str(current_deep))
            if method not in ScriptProcess.ACTIONS.keys():
                msg = "(Deep %s) Could not found Method" % (pre_deep + str(current_deep))
                raise ScriptError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            for key, value in script.items():
                if key.lower() not in ScriptProcess.POP_KEY:
                    temp_args[key] = value
            if pre_return is not None:
                for key, value in temp_args.items():
                    if value == "__PRE_RETURN__":
                        annotation = signature(ScriptProcess.ACTIONS[method]).parameters[key].annotation
                        if pre_return != annotation:
                            msg = f"The pre-return is {pre_return}, But parameter {key} is {annotation}."
                            raise ScriptError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            try:
                pre_return = signature(ScriptProcess.ACTIONS[method]).return_annotation
                ScriptProcess.ACTIONS[method](**temp_args)
            except TypeError as e:
                raise ScriptError(e, method, pre_deep + str(current_deep))
            except AssertionError as e:
                raise ScriptError(e, method, pre_deep + str(current_deep))
            except ParamTypeError as e:
                raise ScriptError(e, method, pre_deep + str(current_deep))
            except Exception:
                pass
            script = script.get("next")

    @staticmethod
    @check
    def generate(scripts: list | dict) -> dict:
        """
        generate the scripts(dict) from list
        """
        if isinstance(scripts, dict):
            return scripts
        res = {}
        temp = res
        for i in range(len(scripts)):
            if "loop" in scripts[i].keys():
                loop_temp = scripts[i]["loop"]
                if "script" in loop_temp:
                    loop_temp["script"] = ScriptProcess.generate(loop_temp["script"])
            temp.update(scripts[i])
            if i != len(scripts) - 1:
                temp["next"] = {}
                temp = temp["next"]
        return res

    @staticmethod
    @check
    def dict2json(scripts_dict: dict) -> str:
        """
        generate the scripts(str of json) from dict
        """
        return json.dumps(scripts_dict)

    @staticmethod
    @check
    def json2dict(scripts_json: str) -> dict:
        """
        generate the scripts(str of json) from dict
        """
        return json.loads(scripts_json)

    @staticmethod
    def add_action(func: callable) -> None:
        if not callable(func):
            raise ParamTypeError("func must be a callable")
        ScriptProcess.ACTIONS[func.__name__] = func


class Script(ScriptProcess):

    @check
    def __init__(self, script: dict | str, interval: float = 0.5):
        """
        Script Parser
        :param script: Need a JSON str or dict that conforms to syntax conventions
        :param interval: The direct interval between two consecutive scripts
        """
        if isinstance(script, str):
            self.script = ScriptProcess.json2dict(script)
        else:
            self.script = script
        ScriptProcess.syntax_check(self.script)
        self.interval = interval

    @check
    def process(self, webdriver: WebDriver) -> Any:
        """
        process the script
        """
        script = self.script
        pre_return = None
        while script:
            temp_args = {"driver": webdriver}
            method = script.get("method")
            for key, value in script.items():
                if key.lower() not in Script.POP_KEY:
                    temp_args[key] = value
            if pre_return is not None:
                for key, value in temp_args.items():
                    if value == "__PRE_RETURN__":
                        temp_args[key] = pre_return
            if "driver" in temp_args and "xpath" in temp_args:
                WebDriverWait(temp_args["driver"], 10).until(
                    EC.presence_of_element_located((By.XPATH, temp_args["xpath"])))
            pre_return = Script.ACTIONS[method](**temp_args)
            script = script.get("next")
            time.sleep(random.uniform(self.interval / 2, self.interval))
        return pre_return

    def __call__(self, webdriver: WebDriver):
        return self.process(webdriver)

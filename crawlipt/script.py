import random
import time
import json
from inspect import signature
from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from crawlipt.annotation import check, ParamTypeError
from crawlipt.action import Action
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def getDriver(is_headless=False):
    option = wd.ChromeOptions()
    arguments = [
        "no-sandbox",
        "--disable-extensions",
        '--disable-gpu',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
        "window-size=1920x3000",
        "start-maximized",
        'cache-control="max-age=0"'
        "disable-blink-features=AutomationControlled"
    ]
    for argument in arguments:
        option.add_argument(argument)
    if is_headless:
        option.add_argument("--headless")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })
    return webdriver


class ScriptError(Exception):
    def __init__(self, e: Exception, method: str, deep: int):
        self.e = e
        self.method = method
        self.deep = deep

    def __str__(self):
        info = ""
        params = ""
        doc = ""
        if self.method:
            params = "\ndef " + self.method + " " + signature(Script.ACTIONS[self.method]).__str__()
            doc = Script.ACTIONS[self.method].__doc__
            info = "----------------------method info--------------------------"
        error = "[" + self.e.__class__.__name__ + "] " + self.e.__str__() + "\n"
        return "(Deep:%d method:%s) arguments is wrong\n" % (self.deep, self.method) + error + info + params + doc


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


class Script:
    ACTIONS = get_action_dict()
    POP_KEY = {"method", "next"}

    @check
    def __init__(self, script: dict | str, interval: float = 0.5):
        """
        Script Parser
        :param script: Need a JSON str or dict that conforms to syntax conventions
        :param interval: The direct interval between two consecutive scripts
        """
        if isinstance(script, str):
            self.script = json.loads(script)
        else:
            self.script = script
        Script.syntax_check(self.script)
        self.interval = interval

    @check
    def process(self, webdriver: WebDriver = None) -> Any:
        """
        process the script
        """
        is_use_default = False
        if not webdriver:
            is_use_default = True
            webdriver = getDriver(is_headless=True)
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
        if is_use_default:
            webdriver.quit()
        return pre_return

    @staticmethod
    @check
    def syntax_check(script: dict | str) -> None:
        """
        Script syntax check
        """
        deep = 0
        pre_return = None
        while script and isinstance(script, dict):
            deep += 1
            temp_args = {"driver": None}
            method = script.get("method")
            if not method:
                msg = "(Deep %d) Method is missing" % deep
                raise ScriptError(ParamTypeError(msg), "", deep)
            for key, value in script.items():
                if key.lower() not in Script.POP_KEY:
                    temp_args[key] = value
            if pre_return is not None:
                for key, value in temp_args.items():
                    if value == "__PRE_RETURN__":
                        annotation = signature(Script.ACTIONS[method]).parameters[key].annotation
                        if pre_return != annotation:
                            msg = f"The pre-return is {pre_return}, But parameter {key} is {annotation}."
                            raise ScriptError(ParamTypeError(msg), method, deep)
            try:
                pre_return = signature(Script.ACTIONS[method]).return_annotation
                Script.ACTIONS[method](**temp_args)
            except TypeError as e:
                raise ScriptError(e, method, deep)
            except AssertionError as e:
                raise ScriptError(e, method, deep)
            except ParamTypeError as e:
                raise ScriptError(e, method, deep)
            except Exception:
                pass
            script = script.get("next")

    @staticmethod
    @check
    def generate(scripts: list) -> dict:
        """
        generate the scripts(dict) from list
        """
        res = {}
        temp = res
        for script in scripts:
            temp.update(script)
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

    def __call__(self, webdriver: WebDriver):
        return self.process(webdriver)

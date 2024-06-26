import random
import time
import json
from inspect import signature
from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from crawlipt.annotation import check, ParamTypeError
from crawlipt.action import Action
from crawlipt.condition import Condition
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import copy
from crawlipt.error import VariableError
from crawlipt.pojo import VariableBase, StoreBase


class ScriptSyntaxError(Exception):
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
        elif self.method and self.method in ScriptProcess.CONDITIONS.keys():
            params = "\ndef " + self.method + " " + signature(Script.CONDITIONS[self.method]).__str__()
            doc = ScriptProcess.CONDITIONS[self.method].__doc__
            info = "----------------------condition info--------------------------"
        error = "[" + self.e.__class__.__name__ + "] " + self.e.__str__() + "\n"
        if not doc:
            doc = ""
        return "(Deep:%s method:%s) arguments is wrong\n" % (self.deep, self.method) + error + info + params + doc


def dfs_search(obj):
    for parent in obj.__bases__:
        if parent == object:
            continue
        dfs_search(parent)
        yield parent.__dict__


def get_dict(obj):
    all_dict = {}
    for element in dfs_search(obj):
        all_dict.update(element)
    for key in list(all_dict.keys()):
        if key.startswith("__") and key.endswith("__"):
            all_dict.pop(key)
    alias_dict = {}
    for value in all_dict.values():
        if "__crawlipt_func_name__" in value.__func__.__dict__:
            alias_dict[value.__func__.__crawlipt_func_name__] = value
    all_dict.update(alias_dict)
    return all_dict


class ScriptProcess:
    ACTIONS = get_dict(Action)
    CONDITIONS = get_dict(Condition)
    __POP_KEY = {"method", "next", "if", "check", "condition", "loop", "return_flag", "while", "fail_script"}

    @staticmethod
    @check
    def __condition_check(temp_condition: dict, name: str, pre_deep: str, current_deep: int,
                          return_record: dict) -> None:
        condition = temp_condition.get("condition")
        temp_args = {"driver": None}
        if not condition:
            msg = "(Deep %s) condition of '%s' is missing" % (pre_deep + str(current_deep), name)
            raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
        if not isinstance(condition, str):
            msg = "(Deep %s) The value of condition must be type of str" % (pre_deep + str(current_deep))
            raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
        if condition.startswith("__not-") and condition.endswith("__"):
            condition = condition[6: -2]
        if condition not in ScriptProcess.CONDITIONS.keys():
            msg = "(Deep %s) Could not found the Condition Method in '%s'" % (pre_deep + str(current_deep), name)
            raise ScriptSyntaxError(ParamTypeError(msg), condition, pre_deep + str(current_deep))
        fail_script = temp_condition.get("fail_script")
        if fail_script:
            ScriptProcess.syntax_check(script=fail_script,
                                       pre_deep=pre_deep + str(current_deep) + "->",
                                       return_record=return_record)
        return_flag = temp_condition.get("return_flag")
        if return_flag and not isinstance(return_flag, str):
            msg = "(Deep %s) return_flag must be the type of str" % (pre_deep + str(current_deep))
            raise ScriptSyntaxError(ParamTypeError(msg), condition, pre_deep + str(current_deep))
        for key, value in temp_condition.items():
            if key.lower() not in ScriptProcess.__POP_KEY:
                temp_args[key] = value
        if "store" in signature(ScriptProcess.CONDITIONS[condition]).parameters:
            temp_args["store"] = None
        if return_record:
            for key, value in temp_args.items():
                if isinstance(value, str) and value.startswith("__rf-") and value.endswith("__"):
                    if value[5:-2] not in return_record.keys():
                        msg = f"The return_flag:{value[5:-2]} cannot be find in history record."
                        raise ScriptSyntaxError(ParamTypeError(msg), condition, pre_deep + str(current_deep))
                    annotation = signature(ScriptProcess.CONDITIONS[condition]).parameters[key].annotation
                    pre_return_flag = return_record[value[5:-2]]
                    if pre_return_flag is Any or annotation is Any:
                        continue
                    if pre_return_flag != annotation:
                        msg = f"The return_flag is {pre_return_flag}, But parameter {key} is {annotation}."
                        raise ScriptSyntaxError(ParamTypeError(msg), condition, pre_deep + str(current_deep))
        try:
            if return_flag:
                return_record[return_flag] = signature(ScriptProcess.CONDITIONS[condition]).return_annotation
            ScriptProcess.CONDITIONS[condition](**temp_args)
        except TypeError as e:
            raise ScriptSyntaxError(e, condition, pre_deep + str(current_deep))
        except AssertionError as e:
            raise ScriptSyntaxError(e, condition, pre_deep + str(current_deep))
        except ParamTypeError as e:
            raise ScriptSyntaxError(e, condition, pre_deep + str(current_deep))
        except Exception:
            pass

    @staticmethod
    @check
    def syntax_check(script: dict | str, pre_deep: str = "", return_record: dict = {}) -> None:
        """
        Script syntax check
        """
        if isinstance(script, str):
            script = json.loads(script)
        current_deep = 0
        pre_return = None
        while script and isinstance(script, dict):
            current_deep += 1
            loop_temp: dict = script.get("loop")
            if loop_temp:
                cnt = loop_temp.get("cnt")
                while_condition = loop_temp.get("while")
                if not cnt and not while_condition:
                    msg = "(Deep %s) loop must set the param of cnt or while" % (pre_deep + str(current_deep))
                    raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
                if while_condition:
                    ScriptProcess.__condition_check(temp_condition=while_condition,
                                                    name="while",
                                                    return_record=return_record,
                                                    pre_deep=pre_deep,
                                                    current_deep=current_deep)
                loop_script = loop_temp.get("script")
                if not loop_script:
                    msg = "(Deep %s) loop must set the param of script" % (pre_deep + str(current_deep))
                    raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
                ScriptProcess.syntax_check(script=loop_script,
                                           pre_deep=pre_deep + str(current_deep) + "->",
                                           return_record=return_record)
            check_condition = script.get("check")
            if check_condition:
                ScriptProcess.__condition_check(temp_condition=check_condition,
                                                name="check",
                                                return_record=return_record,
                                                pre_deep=pre_deep,
                                                current_deep=current_deep)
            if_condition = script.get("if")
            if if_condition:
                if not script.get("method"):
                    msg = "(Deep %s) The 'if' condition must be with a Action Method" % (pre_deep + str(current_deep))
                    raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
                ScriptProcess.__condition_check(temp_condition=if_condition,
                                                name="if",
                                                return_record=return_record,
                                                pre_deep=pre_deep,
                                                current_deep=current_deep)
            temp_args = {"driver": None}
            method = script.get("method")
            if not method:
                script = script.get("next")
                continue
            if not isinstance(method, str):
                msg = "(Deep %s) The value of method must be type of str" % (pre_deep + str(current_deep))
                raise ScriptSyntaxError(ParamTypeError(msg), "", pre_deep + str(current_deep))
            if method not in ScriptProcess.ACTIONS.keys():
                msg = "(Deep %s) Could not found the Action Method" % (pre_deep + str(current_deep))
                raise ScriptSyntaxError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            return_flag = script.get("return_flag")
            if return_flag and not isinstance(return_flag, str):
                msg = "(Deep %s) return_flag must be the type of str" % (pre_deep + str(current_deep))
                raise ScriptSyntaxError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            for key, value in script.items():
                if key.lower() not in ScriptProcess.__POP_KEY:
                    temp_args[key] = value
            if "store" in signature(ScriptProcess.ACTIONS[method]).parameters:
                temp_args["store"] = None
            if pre_return is not None:
                for key, value in temp_args.items():
                    if value == "__PRE_RETURN__":
                        annotation = signature(ScriptProcess.ACTIONS[method]).parameters[key].annotation
                        if pre_return is Any or annotation is Any:
                            continue
                        if pre_return != annotation:
                            msg = f"The pre-return is {pre_return}, But parameter {key} is {annotation}."
                            raise ScriptSyntaxError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            if return_record:
                for key, value in temp_args.items():
                    if isinstance(value, str) and value.startswith("__rf-") and value.endswith("__"):
                        if value[5:-2] not in return_record.keys():
                            msg = f"The return_flag:{value[5:-2]} cannot be find in history record."
                            raise ScriptSyntaxError(ParamTypeError(msg), method, pre_deep + str(current_deep))
                        annotation = signature(ScriptProcess.ACTIONS[method]).parameters[key].annotation
                        pre_return_flag = return_record[value[5:-2]]
                        if pre_return_flag is Any or annotation is Any:
                            continue
                        if pre_return_flag != annotation:
                            msg = f"The return_flag is {pre_return_flag}, But parameter {key} is {annotation}."
                            raise ScriptSyntaxError(ParamTypeError(msg), method, pre_deep + str(current_deep))
            try:
                if signature(ScriptProcess.ACTIONS[method]).return_annotation is not None:
                    pre_return = signature(ScriptProcess.ACTIONS[method]).return_annotation
                if return_flag:
                    return_record[return_flag] = signature(ScriptProcess.ACTIONS[method]).return_annotation
                ScriptProcess.ACTIONS[method](**temp_args)
            except TypeError as e:
                raise ScriptSyntaxError(e, method, pre_deep + str(current_deep))
            except AssertionError as e:
                raise ScriptSyntaxError(e, method, pre_deep + str(current_deep))
            except ParamTypeError as e:
                raise ScriptSyntaxError(e, method, pre_deep + str(current_deep))
            except Exception:
                pass
            script = script.get("next")

    @staticmethod
    @check
    def __process_condition(temp_condition: dict, webdriver: WebDriver, return_record: dict,
                            global_script: dict, interval: float, wait: float, store: StoreBase = None) -> bool:
        condition = temp_condition.get("condition")
        trans_flag = False
        if condition.startswith("__not-") and condition.endswith("__"):
            trans_flag = True
            condition = condition[6: -2]
        return_flag = temp_condition.get("return_flag")
        temp_args = {"driver": webdriver}
        for key, value in temp_condition.items():
            if key.lower() not in ScriptProcess.__POP_KEY:
                temp_args[key] = value
        if "store" in signature(ScriptProcess.CONDITIONS[condition]).parameters:
            temp_args["store"] = store
        if return_record:
            for key, value in temp_args.items():
                if isinstance(value, str) and value.startswith("__rf-") and value.endswith("__"):
                    temp_args[key] = return_record[value[5:-2]]
        is_success = ScriptProcess.CONDITIONS[condition](**temp_args)
        if trans_flag:
            is_success = not is_success
        if return_flag:
            return_record[return_flag] = is_success
        if not is_success:
            fail_script = temp_condition.get("fail_script")
            if fail_script:
                ScriptProcess._process_script(script=fail_script,
                                              global_script=global_script,
                                              webdriver=webdriver,
                                              interval=interval,
                                              return_record=return_record,
                                              wait=wait,
                                              store=store, )
        return is_success

    @staticmethod
    @check
    def _process_script(script: dict, global_script: dict, webdriver: WebDriver, store: StoreBase = None,
                        return_record: dict = {}, interval: float = 0.5, wait: float = 10):
        """
        process the script
        """
        script = copy.deepcopy(script)
        pre_return = None
        while script:
            loop_temp: dict = script.get("loop")
            if loop_temp:
                cnt = loop_temp.get("cnt")
                while_condition = loop_temp.get("while")
                loop_script = loop_temp.get("script")
                if while_condition and cnt:
                    while ScriptProcess.__process_condition(temp_condition=while_condition,
                                                            return_record=return_record,
                                                            global_script=global_script,
                                                            webdriver=webdriver,
                                                            store=store,
                                                            interval=interval,
                                                            wait=wait) and cnt:
                        ScriptProcess._process_script(script=loop_script,
                                                      global_script=global_script,
                                                      webdriver=webdriver,
                                                      return_record=return_record,
                                                      store=store,
                                                      interval=interval,
                                                      wait=wait)
                        cnt -= 1
                if while_condition:
                    while ScriptProcess.__process_condition(temp_condition=while_condition,
                                                            return_record=return_record,
                                                            global_script=global_script,
                                                            webdriver=webdriver,
                                                            store=store,
                                                            interval=interval,
                                                            wait=wait):
                        ScriptProcess._process_script(script=loop_script,
                                                      global_script=global_script,
                                                      webdriver=webdriver,
                                                      return_record=return_record,
                                                      store=store,
                                                      interval=interval,
                                                      wait=wait)
                if cnt:
                    for _ in range(cnt):
                        ScriptProcess._process_script(script=loop_script,
                                                      global_script=global_script,
                                                      webdriver=webdriver,
                                                      return_record=return_record,
                                                      store=store,
                                                      interval=interval,
                                                      wait=wait)
            check_condition = script.get("check")
            if check_condition:
                is_success = ScriptProcess.__process_condition(temp_condition=check_condition,
                                                               return_record=return_record,
                                                               global_script=global_script,
                                                               webdriver=webdriver,
                                                               store=store,
                                                               interval=interval,
                                                               wait=wait)
                if not is_success:
                    return
            if_condition = script.get("if")
            if if_condition:
                is_success = ScriptProcess.__process_condition(temp_condition=if_condition,
                                                               return_record=return_record,
                                                               global_script=global_script,
                                                               webdriver=webdriver,
                                                               store=store,
                                                               interval=interval,
                                                               wait=wait)
                if not is_success:
                    script = script.get("next")
                    continue
            temp_args = {"driver": webdriver}
            method = script.get("method")
            if not method:
                script = script.get("next")
                continue
            for key, value in script.items():
                if key.lower() not in ScriptProcess.__POP_KEY:
                    temp_args[key] = value
            if "store" in signature(ScriptProcess.ACTIONS[method]).parameters:
                temp_args["store"] = store
            if pre_return is not None:
                for key, value in temp_args.items():
                    if value == "__PRE_RETURN__":
                        temp_args[key] = pre_return
            if return_record:
                for key, value in temp_args.items():
                    if isinstance(value, str) and value.startswith("__rf-") and value.endswith("__"):
                        temp_args[key] = return_record[value[5:-2]]
            if "driver" in temp_args and "xpath" in temp_args:
                WebDriverWait(temp_args["driver"], wait).until(
                    EC.presence_of_all_elements_located((By.XPATH, temp_args["xpath"])))
            if "driver" in temp_args and "css" in temp_args:
                WebDriverWait(temp_args["driver"], wait).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, temp_args["css"])))
            if global_script:
                ScriptProcess._process_script(script=global_script,
                                              global_script={},
                                              webdriver=webdriver,
                                              store=store,
                                              interval=interval,
                                              wait=wait)
            current_return = Script.ACTIONS[method](**temp_args)
            if isinstance(store, StoreBase) and current_return:
                store.set(method=method, value=current_return)
            return_flag = script.get("return_flag")
            if return_flag:
                return_record[return_flag] = current_return
            if current_return is not None:
                pre_return = current_return
            script = script.get("next")
            time.sleep(random.uniform(interval / 2, interval))
        return pre_return

    @staticmethod
    @check
    def _replace_variable(script: dict, variable: VariableBase) -> None:
        while script:
            for key in script.keys():
                if key not in ScriptProcess.__POP_KEY and isinstance(script[key], str) and script[key].startswith(
                        "__v-") and script[key].endswith("__"):
                    variable_name = script[key][4:-2]
                    if variable_name not in variable:
                        msg = f"The {variable_name} is not defined."
                        raise VariableError(msg)
                    script[key] = variable.get(variable_name)
            for key in script.keys():
                if key in {"loop", "if", "check", "while", "script", "fail_script"}:
                    ScriptProcess._replace_variable(script=script[key], variable=variable)
            script = script.get("next")

    @staticmethod
    @check
    def generate(scripts: list | dict | str) -> dict:
        """
        generate the scripts(dict) from list
        """
        if isinstance(scripts, dict):
            return scripts
        if isinstance(scripts, str):
            return json.loads(scripts)
        res = {}
        temp = res
        for i in range(len(scripts)):
            for k in scripts[i].keys():
                if k == "loop":
                    loop_temp = scripts[i]["loop"]
                    if "script" in loop_temp:
                        loop_temp["script"] = ScriptProcess.generate(loop_temp["script"])
                if k in {"if", "check", "while"}:
                    judge_temp = scripts[i][k]
                    if "fail_script" in judge_temp:
                        judge_temp["fail_script"] = ScriptProcess.generate(judge_temp["fail_script"])
            temp.update(scripts[i])
            if i != len(scripts) - 1:
                while temp.get("next"):
                    temp = temp.get("next")
                temp["next"] = {}
                temp = temp["next"]
        return res

    @staticmethod
    def generate_json(scripts: dict | list) -> str:
        """
        generate the scripts(str of json) from list or dict.
        """
        return json.dumps(ScriptProcess.generate(scripts))

    @staticmethod
    def add_action(func: callable) -> None:
        """
        add your own action
        """
        if not callable(func):
            raise ParamTypeError("func must be a callable")
        if "driver" not in signature(func).parameters:
            raise ParamTypeError("func must have a 'driver' parameter")
        if "driver" in signature(func).parameters:
            if not issubclass(signature(func).parameters["driver"].annotation, WebDriver):
                raise ParamTypeError("the 'driver' parameter must be a subclass of WebDriver")
        if "store" in signature(func).parameters:
            if not issubclass(signature(func).parameters["store"].annotation, StoreBase):
                raise ParamTypeError("the 'store' parameter must be a subclass of StoreBase")
        if signature(func).parameters["driver"].annotation is not WebDriver:
            raise ParamTypeError("the 'driver' parameter must be a WebDriver of selenium.")
        for name in signature(func).parameters.keys():
            if name in ScriptProcess.__POP_KEY:
                raise ParamTypeError(f"the parameter name: {name} conflicts with the keyword")
        cnt = 0
        if func.__name__ not in ScriptProcess.ACTIONS:
            cnt += 1
            ScriptProcess.ACTIONS[func.__name__] = func
        func_bak = func
        try:
            func = func.__func__
        except Exception:
            pass
        if "__crawlipt_func_name__" in func.__dict__:
            cnt += 1
            ScriptProcess.ACTIONS[func.__crawlipt_func_name__] = func_bak
        if not cnt:
            raise ParamTypeError(f"Add failed")

    @staticmethod
    def add_condition(func: callable) -> None:
        """
        add your own condition
        """
        if not callable(func):
            raise ParamTypeError("func must be a callable")
        if "driver" not in signature(func).parameters:
            raise ParamTypeError("func must have a 'driver' parameter")
        if "driver" in signature(func).parameters:
            if not issubclass(signature(func).parameters["driver"].annotation, WebDriver):
                raise ParamTypeError("the 'driver' parameter must be a subclass of WebDriver")
        if "store" in signature(func).parameters:
            if not issubclass(signature(func).parameters["store"].annotation, StoreBase):
                raise ParamTypeError("the 'store' parameter must be a subclass of StoreBase")
        if signature(func).parameters["driver"].annotation is not WebDriver:
            raise ParamTypeError("the 'driver' parameter must be a WebDriver of selenium.")
        if signature(func).return_annotation is not bool:
            raise ParamTypeError("the return of func must be the type of bool.")
        for name in signature(func).parameters.keys():
            if name in ScriptProcess.__POP_KEY:
                raise ParamTypeError(f"the parameter name: {name} conflicts with the keyword")
        cnt = 0
        if func.__name__ not in ScriptProcess.CONDITIONS:
            cnt += 1
            ScriptProcess.CONDITIONS[func.__name__] = func
        func_bak = func
        try:
            func = func.__func__
        except Exception:
            pass
        if "__crawlipt_func_name__" in func.__dict__:
            cnt += 1
            ScriptProcess.CONDITIONS[func.__crawlipt_func_name__] = func_bak
        if not cnt:
            raise ParamTypeError(f"Add failed")


class Script(ScriptProcess):

    @check
    def __init__(self, script: dict | str | list, global_script: dict | str | list = None, interval: float = 0.5,
                 wait: float = 10, is_need_syntax_check: bool = True):
        """
        Script Parser
        :param script: Need a str of json or dict or list steps that conforms to syntax conventions
        :param global_script: This script will be executed before every actions
        :param interval: The direct interval between two consecutive scripts
        :param wait: The longest wait time before presence of element located
        :param is_need_syntax_check: Whether the script need a syntax check
        """
        self.script = ScriptProcess.generate(script)
        if global_script is None:
            self.global_script = {}
        else:
            self.global_script = ScriptProcess.generate(global_script)
        self.is_need_syntax_check = is_need_syntax_check
        if self.is_need_syntax_check:
            ScriptProcess.syntax_check(self.script)
            ScriptProcess.syntax_check(self.global_script)
        assert interval >= 0
        assert wait >= 0
        self.interval = interval
        self.wait = wait
        self.return_record = {}

    @check
    def process(self, webdriver: WebDriver, variable: VariableBase = None, store: StoreBase = None) -> Any:
        """
        process the script
        """
        self.return_record.clear()
        if self.is_need_syntax_check:
            ScriptProcess.syntax_check(self.script)
            ScriptProcess.syntax_check(self.global_script)
        script = copy.deepcopy(self.script)
        global_script = copy.deepcopy(self.global_script)
        if variable:
            ScriptProcess._replace_variable(script, variable)
            ScriptProcess._replace_variable(global_script, variable)
            if self.is_need_syntax_check:
                ScriptProcess.syntax_check(script)
                ScriptProcess.syntax_check(global_script)
        return ScriptProcess._process_script(script=script,
                                             global_script=global_script,
                                             webdriver=webdriver,
                                             return_record=self.return_record,
                                             store=store,
                                             interval=self.interval,
                                             wait=self.wait)

    def __call__(self, webdriver: WebDriver):
        return self.process(webdriver)

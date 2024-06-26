import random
import time
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Util:

    @staticmethod
    @check(exclude="driver")
    def log(driver: WebDriver, msg: Any) -> None:
        """
        log the msg on the console
        :param driver: selenium webdriver
        :param msg: message to log
        """
        if not driver:
            return
        print(msg)

    @staticmethod
    @check(exclude="driver")
    def interval(driver: WebDriver, num: str | int) -> None:
        """
        delay num seconds
        :param driver: selenium webdriver
        :param num: the interval number
        """
        if not driver:
            return
        if isinstance(num, str):
            num = int(num)
        time.sleep(num)

    @staticmethod
    @check(exclude="driver")
    @alias("interval.random")
    def intervalRandom(driver: WebDriver, num: str | int) -> None:
        """
        delay [num/2, num] seconds
        :param driver: selenium webdriver
        :param num: the interval number
        """
        if not driver:
            return
        if isinstance(num, str):
            num = int(num)
        time.sleep(random.uniform(num / 2, num))

    @staticmethod
    @check(exclude="driver")
    def execute(driver: WebDriver, js: str) -> Any:
        """
        execute the js code
        :param driver: selenium webdriver
        :param js: str of js code text
        """
        return driver.execute_script(js)



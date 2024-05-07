import random
import time

from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check


class Util:

    @staticmethod
    @check(exclude="driver")
    def log(driver: WebDriver, msg: str) -> None:
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
        time.sleep(random.uniform(num / 2, num))

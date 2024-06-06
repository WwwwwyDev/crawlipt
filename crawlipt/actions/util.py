import random
import time
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias
import urllib.request as req
import os


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

    @staticmethod
    @check(exclude="driver")
    def download(driver: WebDriver, url: str, path: str):
        """
        download the file from website
        :param driver: selenium webdriver
        :param url: the link you want to download
        :param path: the path of file you want to save
        """
        if not driver:
            return
        req.urlretrieve(url, path)

    @staticmethod
    @check(exclude="driver")
    def upload(driver: WebDriver, xpath: str, paths: list):
        """
        upload the file from local
        :param driver: selenium webdriver
        :param xpath: the input of upload
        :param paths: the paths of files you want to upload
        """
        for element in paths:
            assert isinstance(element, str)
        element = driver.find_element(By.XPATH, xpath)
        for i in range(len(paths)):
            paths[i] = os.path.realpath(paths[i])
        files = "\n".join(paths)
        element.send_keys(files)

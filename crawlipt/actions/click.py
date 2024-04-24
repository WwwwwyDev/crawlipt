import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check


class Click:
    @staticmethod
    @check(exclude="driver")
    def click(driver: WebDriver, xpath: str) -> None:
        """
        Handling click events
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)

    @staticmethod
    @check(exclude="driver")
    def clickMulti(driver: WebDriver, xpath: str, cnt: str | int, frequency: int = 0.1) -> None:
        """
        Handling click events multiple times
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        :param cnt: click count of the button
        :param frequency: click frequency of the button
        """
        if isinstance(cnt, str):
            cnt = int(cnt)
        element = driver.find_element(By.XPATH, xpath)
        while cnt:
            cnt -= 1
            driver.execute_script("arguments[0].click();", element)
            time.sleep(random.uniform(frequency/2, frequency))



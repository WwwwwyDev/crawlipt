import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from crawlipt.annotation import check, alias


class Click:
    @staticmethod
    @check(exclude="driver")
    def click(driver: WebDriver, xpath: str) -> None:
        """
        Handling click events of first element
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        element = driver.find_element(By.XPATH, xpath)
        element.click()

    @staticmethod
    @check(exclude="driver")
    @alias("click.multi")
    def clickMulti(driver: WebDriver, xpath: str, cnt: str | int, frequency: float = 0.1) -> None:
        """
        Handling click events of first element multiple times
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
            element.click()
            time.sleep(random.uniform(frequency / 2, frequency))

    @staticmethod
    @check(exclude="driver")
    @alias("click.js")
    def clickByJs(driver: WebDriver, xpath: str) -> None:
        """
        Handling click events of first element by js 'arguments[0].click();'
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)

    @staticmethod
    @check(exclude="driver")
    @alias("click.all")
    def clickAll(driver: WebDriver, xpath: str) -> None:
        """
        Handling click events of all element
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        elements = driver.find_elements(By.XPATH, xpath)
        for element in elements:
            if EC.element_to_be_clickable(element):
                element.click()

    @staticmethod
    @check(exclude="driver")
    @alias("click.all.js")
    def clickAllByJs(driver: WebDriver, xpath: str) -> None:
        """
        Handling click events of all element by js 'arguments[0].click();'
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        elements = driver.find_elements(By.XPATH, xpath)
        for element in elements:
            driver.execute_script("arguments[0].click();", element)

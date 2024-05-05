from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Input:
    @staticmethod
    @check(exclude="driver")
    @alias("I")
    def input(driver: WebDriver, xpath: str, text: str) -> None:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :param text: text needs to be passed in
        """
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(text)

    @staticmethod
    @check(exclude="driver")
    @alias("E")
    def enter(driver: WebDriver, xpath: str) -> None:
        """
        Press the enter key once
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :return: Whether successful
        """
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(Keys.RETURN)

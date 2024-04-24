from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check


class Get:

    @staticmethod
    @check(exclude="driver")
    def getInnerText(driver: WebDriver, xpath: str) -> str:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the element
        """
        element = driver.find_element(By.XPATH, xpath)
        res = element.get_attribute('innerText')
        if res is None:
            res = ""
        return res

    @staticmethod
    @check(exclude="driver")
    def getTextContent(driver: WebDriver, xpath: str) -> str:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the element
        """
        element = driver.find_element(By.XPATH, xpath)
        res = element.get_attribute('textContent')
        if res is None:
            res = ""
        return res

    @staticmethod
    @check(exclude="driver")
    def getAttribute(driver: WebDriver, xpath: str, name: str) -> str:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the element
        :param name: The name of the attribute
        """
        element = driver.find_element(By.XPATH, xpath)
        res = element.get_attribute(name)
        if res is None:
            res = ""
        return res

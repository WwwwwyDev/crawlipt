from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Get:

    @staticmethod
    @check(exclude="driver")
    @alias("get.innerText")
    def getInnerText(driver: WebDriver, xpath: str) -> str:
        """
        get inner text of element
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
    @alias("get.textContent")
    def getTextContent(driver: WebDriver, xpath: str) -> str:
        """
        get text content of element
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
    @alias("get.attribute")
    def getAttribute(driver: WebDriver, xpath: str, name: str) -> str:
        """
        get the attribute of an element
        :param driver: selenium webdriver
        :param xpath: The xpath path of the element
        :param name: The name of the attribute
        """
        element = driver.find_element(By.XPATH, xpath)
        res = element.get_attribute(name)
        if res is None:
            res = ""
        return res



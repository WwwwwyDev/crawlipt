from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select as WebSelect
from crawlipt.annotation import check


class Select:
    @staticmethod
    @check(exclude="driver")
    def selectByText(driver: WebDriver, xpath: str, text: str) -> None:
        """
        Handling select events
        :param driver: selenium webdriver
        :param xpath: the xpath path of the select element
        :param text: the text of selecting
        """
        select = WebSelect(driver.find_element(By.XPATH, xpath))
        select.select_by_visible_text(text)

    @staticmethod
    @check(exclude="driver")
    def selectByValue(driver: WebDriver, xpath: str, value: str) -> None:
        """
        Handling select events
        :param driver: selenium webdriver
        :param xpath: the xpath path of the select element
        :param value: the value of selecting
        """
        select = WebSelect(driver.find_element(By.XPATH, xpath))
        select.select_by_value(value)

    @staticmethod
    @check(exclude="driver")
    def selectByIndex(driver: WebDriver, xpath: str, index: int) -> None:
        """
        Handling select events
        :param driver: selenium webdriver
        :param xpath: the xpath path of the select element
        :param index: the index of selecting
        """
        select = WebSelect(driver.find_element(By.XPATH, xpath))
        select.select_by_index(index)

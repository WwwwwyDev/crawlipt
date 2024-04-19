from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check


class Input:
    @staticmethod
    @check(exclude="driver")
    def input(driver: WebDriver, xpath: str, keyword: str) -> None:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :param keyword: keyword needs to be passed in
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(keyword)

    @staticmethod
    @check(exclude="driver")
    def enter(driver: WebDriver, xpath: str) -> None:
        """
        Press the enter key once
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :return: Whether successful
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(Keys.RETURN)
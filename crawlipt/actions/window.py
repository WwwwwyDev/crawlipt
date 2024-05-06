from selenium.common import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Window:
    @staticmethod
    @check(exclude="driver")
    def clear(driver: WebDriver) -> None:
        """
        close all windows
        :param driver: selenium webdriver
        """
        for _ in range(driver.window_handles.__len__()-1):
            driver.close()
        driver.get("data:,")

    @staticmethod
    @check(exclude="driver")
    def back(driver: WebDriver) -> None:
        """
        Goes one step backward in the browser history.
        :param driver: selenium webdriver
        """
        driver.back()

    @staticmethod
    @check(exclude="driver")
    def forword(driver: WebDriver) -> None:
        """
        Goes one step forward in the browser history.
        :param driver: selenium webdriver
        """
        driver.forward()

    @staticmethod
    @check(exclude="driver")
    def close(driver: WebDriver) -> None:
        """
        Closes the current window.
        :param driver: selenium webdriver
        """
        driver.close()

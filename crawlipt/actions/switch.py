from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check


class Switch:
    @staticmethod
    @check(exclude="driver")
    def switchLastTab(driver: WebDriver) -> None:
        """
        Switch to the last handle
        :param driver: selenium webdriver
        """
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])

    @staticmethod
    @check(exclude="driver")
    def switchTab(driver: WebDriver, index: int) -> None:
        """
        Switch to the index handle
        :param driver: selenium webdriver
        :param index: The index handle
        """
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[index])

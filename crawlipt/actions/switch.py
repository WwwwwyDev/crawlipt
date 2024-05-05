from selenium.webdriver.common.by import By
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
    def switchTab(driver: WebDriver, index: int | str) -> None:
        """
        Switch to the index handle
        :param driver: selenium webdriver
        :param index: The index handle
        """
        if isinstance(index, str):
            index = int(index)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[index])

    @staticmethod
    @check(exclude="driver")
    def switchToFrame(driver: WebDriver, xpath: str) -> None:
        """
        Switch to the inner frame
        :param driver: selenium webdriver
        :param xpath: The xpath of frame
        """
        frame = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(frame)

    @staticmethod
    @check(exclude="driver")
    def switchOutFrame(driver: WebDriver) -> None:
        """
        Switch to the outer frame
        :param driver: selenium webdriver
        """
        driver.switch_to.parent_frame()

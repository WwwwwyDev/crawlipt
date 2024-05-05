from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check, alias


class Element:

    @staticmethod
    @check(exclude="driver")
    @alias("clickable")
    def element_to_be_clickable(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An Expectation for checking an element is visible and enabled such that you can click it.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            return True
        except Exception:
            return False

    @staticmethod
    @check(exclude="driver")
    @alias("selected")
    def element_located_to_be_selected(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An Expectation for checking an element is visible and enabled such that you can click it.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.element_located_to_be_selected((By.XPATH, xpath)))
            return True
        except Exception:
            return False
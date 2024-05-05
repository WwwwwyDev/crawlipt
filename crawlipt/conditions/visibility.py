from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check, alias


class Visibility:

    @staticmethod
    @check(exclude="driver")
    @alias("visibility")
    def visibility_of_element_located(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An expectation for checking that an element is present on the DOM of a page and visible.Visibility means that the element is not only displayed but also has a height and width that is greater than 0.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except Exception:
            return False

    @staticmethod
    @check(exclude="driver")
    @alias("invisibility")
    def invisibility_of_element_located(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An Expectation for checking that an element is either invisible or not present on the DOM.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.invisibility_of_element_located((By.XPATH, xpath)))
            return True
        except Exception:
            return False
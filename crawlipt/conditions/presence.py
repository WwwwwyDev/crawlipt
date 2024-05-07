from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check, alias


class Presence:

    @staticmethod
    @check(exclude="driver")
    @alias("presence")
    def presence_of_element_located(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An expectation for checking that an element is present on the DOM of a page. This does not necessarily mean that the element is visible.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception:
            return False

    @staticmethod
    @check(exclude="driver")
    @alias("presences")
    def presence_of_all_elements_located(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An expectation for checking that there is at least one element present on a web page.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return True
        except Exception:
            return False

    @staticmethod
    @check(exclude="driver")
    def alert_is_present(driver: WebDriver, wait: float = 1) -> bool:
        """
        An expectation for checking whether the given frame is available to switch to.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.alert_is_present())
            return True
        except Exception:
            return False


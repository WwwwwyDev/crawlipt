from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check


class Text:

    @staticmethod
    @check(exclude="driver")
    def text_to_be_present_in_element(driver: WebDriver, xpath: str, text: str, wait: float = 1) -> bool:
        """
        An expectation for checking if the given text is present in the specified element.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.text_to_be_present_in_element((By.XPATH, xpath), text))
            return True
        except Exception:
            return False

    @staticmethod
    @check(exclude="driver")
    def text_to_be_present_in_element_value(driver: WebDriver, xpath: str, value: str, wait: float = 1) -> bool:
        """
        An expectation for checking if the given text is present in the element's value.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.text_to_be_present_in_element_value((By.XPATH, xpath), value))
            return True
        except Exception:
            return False
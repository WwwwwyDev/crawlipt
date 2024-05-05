from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check


class Frame:

    @staticmethod
    @check(exclude="driver")
    def frame_to_be_available_and_switch_to_it(driver: WebDriver, xpath: str, wait: float = 1) -> bool:
        """
        An expectation for checking whether the given frame is available to switch to.
        """
        try:
            WebDriverWait(driver, wait).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
            return True
        except Exception:
            return False

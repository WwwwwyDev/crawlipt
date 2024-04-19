from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from crawlipt.annotation import check


class Click:
    @staticmethod
    @check(exclude="driver")
    def click(driver: WebDriver, xpath: str,) -> None:
        """
        Handling click events
        :param driver: selenium webdriver
        :param xpath: click on the xpath path of the button
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)

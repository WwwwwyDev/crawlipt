from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from crawlipt.annotation import check


class Slide:
    @staticmethod
    @check(exclude="driver")
    def slide(driver: WebDriver, xpath: str, position: list) -> None:
        """
        Handling click events
        :param driver: selenium webdriver
        :param xpath: The element to be slid
        :param position: The x, y position
        """
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        slider = driver.find_element(By.XPATH, xpath)
        if len(position) != 2:
            return
        x, y = position
        start_x = slider.location["x"]
        end_x = start_x + x
        distance_x = end_x - start_x
        start_y = slider.location["y"]
        end_y = start_y + y
        distance_y = end_y - start_y
        action_chains = ActionChains(driver)
        action_chains.click_and_hold(slider).move_by_offset(distance_x, distance_y).release().perform()

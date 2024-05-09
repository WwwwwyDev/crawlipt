import random
import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check


class Scroll:

    @staticmethod
    @check(exclude="driver")
    def scrollByJs(driver: WebDriver, height: str | int) -> None:
        """
        Handling scroll events by Js
        :param driver: selenium webdriver
        :param height: scroll height
        """
        height = str(height)
        js_code = "document.documentElement.scrollTop += %s" % height
        driver.execute_script(js_code)

    @staticmethod
    @check(exclude="driver")
    def scrollBySpace(driver: WebDriver, cnt: str | int, frequency: int = 0.1) -> None:
        """
        Handling scroll events by space
        :param driver: selenium webdriver
        :param cnt: the cnt of space
        :param frequency: the frequency of space
        """
        if isinstance(cnt, str):
            cnt = int(cnt)
        actions = ActionChains(driver)
        actions.move_by_offset(0, 0).click().perform()
        time.sleep(random.uniform(frequency / 2, frequency))
        for _ in range(cnt):
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.uniform(frequency / 2, frequency))

    @staticmethod
    @check(exclude="driver")
    def scrollToBottom(driver: WebDriver) -> None:
        """
        Handling scroll to bottom events by Js
        :param driver: selenium webdriver
        """
        js_code = '''he = setInterval(() => {
                            document.documentElement.scrollTop += document.documentElement.scrollHeight
                            if (document.documentElement.scrollTop >= (document.documentElement.scrollHeight - document.documentElement.scrollWidth)) {
                                clearInterval(he)
                            }
                        },100)
                    '''
        driver.execute_script(js_code)

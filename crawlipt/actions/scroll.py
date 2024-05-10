import random
import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Scroll:

    @staticmethod
    @check(exclude="driver")
    @alias("scroll.js")
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
    @alias("scroll.space")
    def scrollBySpace(driver: WebDriver, cnt: str | int, frequency: float = 0.1) -> None:
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
    @alias("scroll.bottom")
    def scrollToBottom(driver: WebDriver) -> None:
        """
        Handling scroll to bottom events by Js
        :param driver: selenium webdriver
        """
        js_code = '''window.scrollTo({
                        top: document.documentElement.scrollHeight,
                        left: 0,
                        behavior: 'smooth' // 可选，平滑滚动效果
                      });
                    '''
        driver.execute_script(js_code)

    @staticmethod
    @check(exclude="driver")
    @alias("scroll.top")
    def scrollToTop(driver: WebDriver) -> None:
        """
        Handling scroll to top events by Js
        :param driver: selenium webdriver
        """
        js_code = '''window.scrollTo({
                        top: 0,
                        left: 0,
                        behavior: 'smooth' // 可选，平滑滚动效果
                      });
                    '''
        driver.execute_script(js_code)

    @staticmethod
    @check(exclude="driver")
    @alias("scroll.arrow.up")
    def scrollUpByArrow(driver: WebDriver, cnt: str | int, frequency: float = 0.1) -> None:
        """
        Handling scroll events by arrow
        :param driver: selenium webdriver
        :param cnt: the cnt of arrow
        :param frequency: the frequency of arrow
        """
        if isinstance(cnt, str):
            cnt = int(cnt)
        actions = ActionChains(driver)
        for _ in range(cnt):
            actions.send_keys(Keys.ARROW_UP).perform()
            time.sleep(random.uniform(frequency / 2, frequency))

    @staticmethod
    @check(exclude="driver")
    @alias("scroll.arrow.down")
    def scrollDownByArrow(driver: WebDriver, cnt: str | int, frequency: float = 0.1) -> None:
        """
        Handling scroll events by arrow
        :param driver: selenium webdriver
        :param cnt: the cnt of arrow
        :param frequency: the frequency of arrow
        """
        if isinstance(cnt, str):
            cnt = int(cnt)
        actions = ActionChains(driver)
        for _ in range(cnt):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(random.uniform(frequency / 2, frequency))

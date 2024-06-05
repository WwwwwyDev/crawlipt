from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Redirect:
    @staticmethod
    @check(exclude="driver")
    @alias("redirect.search")
    def searchRedirect(driver: WebDriver, url: str, keyword: str) -> None:
        """
        Replace % s in the path with keyword and redirect it
        :param driver:  selenium webdriver
        :param url: Link containing %s
        :param keyword: keyword needs to be passed in
        """
        url = url.replace(r"%s", keyword)
        driver.get(url)

    @staticmethod
    @check(exclude="driver")
    def redirect(driver: WebDriver, url: str) -> None:
        """
        Direct redirection
        :param driver:  selenium webdriver
        :param url: Links that require redirection
        """
        driver.get(url)

    @staticmethod
    @check(exclude="driver")
    @alias("redirect.js")
    def redirectByJs(driver: WebDriver, url: str) -> None:
        """
        Direct redirection by js
        :param driver:  selenium webdriver
        :param url: Links that require redirection
        """
        js = f"window.location.href = '{url}'"
        driver.execute_script(js)

    @staticmethod
    @check(exclude="driver")
    @alias("redirect.new")
    def redirectNewTab(driver: WebDriver, url: str) -> None:
        """
        redirect to a new tab
        :param driver:  selenium webdriver
        :param url: Links that require redirection
        """
        js = f'window.open("{url}")'
        driver.execute_script(js)
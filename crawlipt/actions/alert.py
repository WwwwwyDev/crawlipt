from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawlipt.annotation import check, alias


class Alert:
    @staticmethod
    @check(exclude="driver")
    def alert(driver: WebDriver, operation: str, text: str = "") -> str:
        """
        Handling alert events
        :param driver: selenium webdriver
        :param operation: option in ["dismiss", "accept"]
        :param text: text to input
        """
        assert operation == "dismiss" or operation == "accept"
        alert = driver.switch_to.alert
        if text:
            alert.send_keys(text)
        if operation == "dismiss":
            alert.dismiss()
        else:
            alert.accept()
        return alert.text


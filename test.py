import unittest

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt


class TestCase(unittest.TestCase):
    def test_01(self):
        option = wd.ChromeOptions()
        option.add_argument("start-maximized")
        # option.add_argument("--headless")
        option.add_argument("window-size=1920x3000")
        agent = 'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
        option.add_argument(agent)
        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        script = {
            "method": "redirect",
            "url": "https://www.baidu.com/",
            "next": {
                "method": "input",
                "xpath": "//*[@id=\"kw\"]",
                "keyword": "和泉雾纱",
                "next": {
                    "method": "click",
                    "xpath": "//*[@id=\"su\"]"
                }
            }
        }
        cpt.Script(script, interval=2)(webdriver)
        webdriver.quit()


if __name__ == '__main__':
    unittest.main()

import time
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
                "text": "百度贴吧",
                "next": {
                    "method": "click",
                    "xpath": "//*[@id=\"su\"]"
                }
            }
        }
        cpt.Script(script, interval=2)(webdriver)
        print(script)
        webdriver.quit()

    def test_02(self):
        script = {
            "method": "redirect",
            "url": "https://www.baidu.com/",
            "next": {
                "method": "input",
                "xpath": "//*[@id=\"kw\"]",
                "text": "__PRE_RETURN__",
                "next": {
                    "method": "click",
                    "xpath": "//*[@id=\"su\"]"
                }
            }
        }
        cpt.Script(script, interval=2)
        print(script)

    def test_03(self):
        option = wd.ChromeOptions()
        option.add_argument("start-maximized")
        # option.add_argument("--headless")
        option.add_argument("window-size=1920x3000")
        agent = 'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
        option.add_argument(agent)
        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        step = [{
            "method": "redirect",
            "url": "https://accounts.douban.com/passport/login",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"account\"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"username\"]",
            "text": "773323518@qq.com",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"password\"]",
            "text": "testtest",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"account\"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a",
        }, {
            "method": "switchToframe",
            "xpath": "//*[@id=\"tcaptcha_iframe_dy\"]",
        }, {"method": "slide",
            "xpath": "//*[@id=\"tcOperation\"]/div[6]/img",
            "position": [20, 0]}]
        script = cpt.Script.generate(step)
        print(script)
        cpt.Script(script, interval=2)(webdriver)
        print(script)
        webdriver.quit()

    def test_04(self):
        option = wd.ChromeOptions()
        arguments = [
            "no-sandbox",
            "--disable-extensions",
            '--disable-gpu',
            'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
            "window-size=1920x3000",
            "start-maximized",
            'cache-control="max-age=0"'
            "disable-blink-features=AutomationControlled"
        ]
        for argument in arguments:
            option.add_argument(argument)
        # option.add_argument("--headless")
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => false
            })
          """
        })
        step = [{
            "method": "redirect",
            "url": "https://www.boc.cn/sourcedb/whpj/",
        }, {
            "method": "selectByText",
            "xpath": "//*[@id=\"pjname\"]",
            "text": "新加坡元"
        },]
        script = cpt.Script.generate(step)
        print(script)
        cpt.Script(script, interval=5)(webdriver)
        print(script)
        webdriver.quit()

if __name__ == '__main__':
    unittest.main()

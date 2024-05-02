import random
import unittest

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt
import ddddocr as docr


def get_driver(is_headless=False, is_eager=False):
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
    if is_headless:
        option.add_argument("--headless")
    if not is_eager:
        option.page_load_strategy = 'eager'
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })
    return webdriver


def get_remote_driver(webdriver_url, is_eager=False) -> WebDriver:
    option = wd.ChromeOptions()
    arguments = [
        "no-sandbox",
        "--disable-extensions",
        '--disable-gpu',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
        "window-size=1920x3000",
        "start-maximized",
        'cache-control="max-age=0"',
        "disable-blink-features=AutomationControlled"
    ]
    for argument in arguments:
        option.add_argument(argument)
    option.add_argument("--headless")
    if not is_eager:
        option.page_load_strategy = 'eager'
    option.set_capability('cloud:options', DesiredCapabilities.CHROME)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver = wd.Remote(command_executor=webdriver_url, options=option)
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => false
            })
          """
    })
    webdriver.implicitly_wait(10)
    return webdriver


class TestCase(unittest.TestCase):
    def test_01(self):
        webdriver = get_driver()
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
        cpt.Script(script, interval=0.1)(webdriver)
        webdriver.quit()

    def test_02(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://www.boc.cn/sourcedb/whpj/",
        }, {
            "method": "selectByText",
            "xpath": "//*[@id=\"pjname\"]",
            "text": "新加坡元"
        }, ]
        cpt.Script(step, interval=0.1)(webdriver)
        webdriver.quit()

    def test_03(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://accounts.douban.com/passport/login",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"account\"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"username\"]",
            "text": "testtest@gmail.com",
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
            "position": [30, 0]}]
        cpt.Script(step, interval=0.1)(webdriver)
        webdriver.quit()

    def test_04(self):
        webdriver = get_driver(is_headless=True)
        step = [{
            "method": "redirect",
            "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
        }, {
            "method": "redirect",
            "url": "https://fanyi.baidu.com/mtpe-individual/multimodal#/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"editor-text\"]/div[1]/div[1]/div/div/div/div",
            "text": "你好，世界",
        }, {
            "method": "getInnerText",
            "xpath": "//*[@id=\"trans-selection\"]/div/span",
        }]
        result = cpt.Script(step, interval=0.1)(webdriver)
        print(result)
        webdriver.quit()

    def test05(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://www.psy525.cn/ceshi/84307.html",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"fun\"]/a"
        }]
        for i in range(90):
            index = random.randint(1, 5)
            step.append({
                "method": "click",
                "xpath": f"//*[@id=\"question_{i + 1}\"]/fieldset/ul/li[{index}]"
            })
        cpt.Script(step, interval=1)(webdriver)
        webdriver.quit()

    def test06(self):
        webdriver = get_driver()

        @cpt.check(exclude="driver")
        def crackCaptcha(driver: WebDriver, xpath: str) -> str:
            """
            Handling keyboard input events
            :param driver: selenium webdriver
            :param xpath: The xpath path of the captcha
            """
            element = driver.find_element(By.XPATH, xpath)
            pic = element.screenshot_as_png
            ocr = docr.DdddOcr(show_ad=False)
            res = ocr.classification(pic)
            return res

        cpt.Script.add_action(crackCaptcha)
        step = [{
            "method": "redirect",
            "url": "http://www.shuhai.com/login",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"login_form\"]/div[2]/div[1]/div[2]/input",
            "text": "username",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"login_form\"]/div[2]/div[2]/div[2]/input",
            "text": "password",
        }, {
            "method": "crackCaptcha",
            "xpath": "//*[@id=\"checkcode2\"]",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"login_form\"]/div[2]/div[3]/div[2]/input",
            "text": "__PRE_RETURN__"
        }, {
            "method": "click",
            "xpath": "//*[@id=\"dosubmit\"]",
        }]
        cpt.Script(step, interval=1)(webdriver)
        webdriver.quit()

    def test07(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://artsandculture.google.com/",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[1]/div[3]/div[2]/span/span",
        }, {
            "method": "getInnerText",
            "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/div[3]/div/ul/div/li[1]/a"
        }, {
            "method": "input",
            "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
            "text": "__PRE_RETURN__",
        }, {
            "method": "enter",
            "xpath": "//*[@id=\"yDmH0d\"]/div[2]/div[2]/div/input",
        }]
        cpt.Script(step, interval=1)(webdriver)
        webdriver.quit()

    def test_loop(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://www.bchrt.com/tools/click-counter/",
        }, {
            "loop": {
                "cnt": 5,
                "script": [{
                    "loop": {
                        "cnt": 2,
                        "script": {
                            "method": "click",
                            "xpath": "//*[@id=\"addbtn\"]",
                        },
                    }
                },
                    {
                        "method": "click",
                        "xpath": "//*[@id=\"subbtn\"]",
                    }
                ]
            }
        }]
        cpt.Script(step)(webdriver)
        webdriver.quit()


if __name__ == '__main__':
    unittest.main()

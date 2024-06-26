import random
import unittest

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
import crawlipt as cpt
import crawlist as cl
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
            "method": "switchToFrame",
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
        result = cpt.Script(step, interval=0)(webdriver)
        print(result)
        webdriver.quit()

    def test05(self):
        webdriver = get_driver(is_headless=True)
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

        class A:
            @staticmethod
            @cpt.check(exclude="driver")
            @cpt.alias("captcha")
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

        cpt.Script.add_action(A.crackCaptcha)
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
        result = cpt.Script(step, interval=1)(webdriver)
        print(result)
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

        @cpt.check(exclude="driver")
        def checkNum(driver: WebDriver, xpath: str) -> bool:
            """
            your doc
            :param driver: selenium webdriver
            :param xpath: the xpath of element
            """
            element = driver.find_element(By.XPATH, xpath)
            value = int(element.get_attribute("value"))
            if value > 10:
                return False
            else:
                return True

        cpt.Script.add_condition(checkNum)

        step = [{
            "method": "redirect",
            "url": "https://www.bchrt.com/tools/click-counter/",
        }, {
            "method": "getAttribute",
            "xpath": "//*[@id=\"count\"]",
            "name": "value",
            "loop": {
                "while": {
                    "condition": "checkNum",
                    "xpath": "//*[@id=\"count\"]"
                },
                "script": [{
                    "loop": {
                        "cnt": 5,
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
        json_str = cpt.Script.generate_json(step)
        res = cpt.Script(json_str)(webdriver)
        print(res)
        webdriver.quit()

    def test_conditions(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://www.baidu.com/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "text": "1",
            "check": {
                "condition": "__not-presence__",
                "xpath": "//*[@id=\"su\"]"
            }
        }, {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "text": "  2",
        }]
        cpt.Script(step, interval=3)(webdriver)

    def test_variable(self):
        webdriver = get_driver()
        step = [{
            "method": "redirect",
            "url": "https://www.baidu.com/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "text": "__v-searchKey__",
            "if": {
                "condition": "presence",
                "xpath": "__v-button_xpath__"
            }
        }, {
            "method": "clear"
        }]
        v1 = cpt.Variable({
            "searchKey": "hello",
            "button_xpath": "//*[@id=\"su\"]"
        })
        v2 = cpt.Variable({
            "searchKey": "world",
            "button_xpath": "//*[@id=\"su\"]"
        })
        v3 = cpt.Variable({
            "searchKey": "world",
            "button_xpath": "//*[@id=\"su_no_existence\"]"
        })
        loader = cpt.Script(step, interval=3)
        loader.process(webdriver=webdriver,
                       variable=v1)
        loader.process(webdriver=webdriver,
                       variable=v2)
        loader.process(webdriver=webdriver,
                       variable=v3)
        webdriver.quit()

    def test_store(self):

        class MyStore(cpt.StoreBase):
            def __init__(self):
                self.data = []

        @cpt.check(exclude=["driver", "store"])
        def crawl_baidu_list(driver: WebDriver, store: MyStore, limit: int) -> None:
            if not driver:
                return None
            pager = cl.DynamicNumButtonPager(button_selector=cl.XpathWebElementSelector('//*[@id="page"]/div/a/span'),
                                             webdriver=driver, interval=2)
            selector = cl.CssSelector(pattern="#content_left > div")
            analyzer = cl.AnalyzerPrettify(pager, selector)
            for e in analyzer(limit):
                store.data.append(e)

        cpt.Script.add_action(crawl_baidu_list)
        webdriver = get_driver(is_headless=True)
        step = [{
            "method": "redirect",
            "url": "https://www.baidu.com/",
        }, {
            "method": "input",
            "xpath": "//*[@id=\"kw\"]",
            "text": "__v-keyword__",
        }, {
            "method": "click",
            "xpath": "//*[@id=\"su\"]"
        }, {
            "method": "crawl_baidu_list",
            "limit": "__v-limit__",
        }, {
            "method": "clear"
        }]
        v1 = cpt.Variable({
            "limit": 20,
            "keyword": "和泉雾纱"
        })
        store1 = MyStore()
        v2 = cpt.Variable({
            "limit": 20,
            "keyword": "python"
        })
        store2 = MyStore()
        loader = cpt.Script(step, interval=1)
        loader.process(webdriver=webdriver, store=store1, variable=v1)
        print(store1.data)
        loader.process(webdriver=webdriver, store=store2, variable=v2)
        print(store2.data)
        webdriver.quit()

    def test_08(self):
        js_code1 = '''
                     var element = document.querySelector("body > div > main > div.row.justify-content-center.pt-2.pb-3.-bg-selenium-cyan > div > div > h2");
                     return element.innerText;
                    '''
        js_code2 = '''
                     return 1
                    '''
        step = [{
            "method": "redirect",
            "url": "https://www.selenium.dev/",
        }, {
            "method": "execute",
            "js": "__v-js_code__",
        }, {
            "method": "log",
            "msg": "__PRE_RETURN__"
        }]

        v1 = cpt.Variable({
            "js_code": js_code1,
        })
        v2 = cpt.Variable({
            "js_code": js_code2,
        })
        webdriver = get_driver(is_headless=True)
        loader = cpt.Script(step, interval=3)
        s = cpt.Store(is_replace=True)
        print(type(loader.process(webdriver, variable=v1, store=s)))
        print(type(loader.process(webdriver, variable=v2, store=s)))
        print(s.data)
        webdriver.quit()


if __name__ == '__main__':
    unittest.main()

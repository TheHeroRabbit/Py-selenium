import os
import uuid
import random

from time import sleep
from . import save_data
from pathlib import Path
from ddddocr import DdddOcr
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

USER_DATA_DIR = Path.cwd().joinpath(".cache")


class AutoChrome:

    def __init__(self, mode, userdataDir=None):
        """
        构造函数
        """
        options = self.NewChromeOptions(mode, userdataDir)
        service = Service(executable_path="chromedriver.exe")

        self.driver = Chrome(options=options,
                             service=service,)

        # self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        # self.driver.set_window_size(1366, 768)
        self.actions = ActionChains(self.driver)

    @staticmethod
    def NewChromeOptions(mode, folder) -> Options:
        """
        初始设置
        """
        folder = folder if folder else str(uuid.uuid4())
        __user_data_dir = USER_DATA_DIR.joinpath(folder)

        options = Options()

        if 'dev' in mode:
            if 'start' in mode:
                os.popen("taskkill /f /im chromedriver.exe")
                os.popen("taskkill /f /im chrome.exe")
                sleep(1)
                os.popen(f'start chrome.exe --remote-debugging-port=62222 --user-data-dir="{__user_data_dir}"')

            options.add_experimental_option(
                "debuggerAddress",
                "127.0.0.1:62222",
            )
            return options

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir={}".format(__user_data_dir))
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        return options

    def WaitElementAppear(self, x_path) -> WebElement:
        """
        等待元素可见
        """
        locator = (By.XPATH, x_path)
        element = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located(locator))

        return element

    def WaitElementDisappear(self, x_path):
        """
        等待元素消失
        """
        try:
            self.driver.implicitly_wait(0)
            element = self.driver.find_element(By.XPATH, x_path)
            for _ in range(20):
                sleep(1)
                if not element.is_enabled():
                    break
        except:
            pass
        finally:
            self.driver.implicitly_wait(30)

    def ClickElement(self, x_path, n=1):
        """
        元素点击
        """
        element = self.WaitElementAppear(x_path)
        self.actions.move_to_element(element).click(on_element=element).pause(n).perform()

    def InputElement(self, x_path, value):
        """
        元素输入
        """
        element = self.WaitElementAppear(x_path)
        element.clear()
        element.send_keys(value, Keys.ENTER)

    def SetElementValue(self, x_path, value):
        """
        设置元素文本
        """
        element = self.WaitElementAppear(x_path)
        self.driver.execute_script("arguments[0].focus();", element)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
        self.driver.execute_script("arguments[0].blur();", element)

    def RecognizeCodeImg(self, x_path):
        """
        识别验证码
        """
        element = self.WaitElementAppear(x_path)
        imgfile = element.screenshot_as_base64

        ocr = DdddOcr(show_ad=False)
        result = ocr.classification(imgfile)

        return result

    @save_data('baiduTest')
    def baiduTest(self):
        """
        百度测试
        """
        self.driver.get("https://www.baidu.com/")
        self.InputElement('//*[@id="kw"]', 'python')
        self.ClickElement('//*[@id="su"]')

        for n in range(6):
            self.ClickElement('//a[contains(text(),"下一页")]', n=2.5)
            yield {'status': 'next page', 'message': f'第{n+1}页...'}

        yield {'status': 'over', 'message': '百度翻页测试结束'}

        sleep(1)
        self.driver.quit()

    @save_data('formTest')
    def formTest(self):
        """
        表单测试
        """
        self.driver.get("http://www.vrbrothers.com/cn/wqm/demo/pages/Demo-ComplexForm.aspx")

        for _ in range(20):

            self.SetElementValue('//*[@id="ctl00_mainContent_tbUsername"]', random.choice(['李雷', '韩梅梅']))
            self.SetElementValue('//*[@id="ctl00_mainContent_tbPassword"]', str(random.randint(10000, 99999)))
            self.SetElementValue('//*[@id="ctl00_mainContent_tbEMail"]', '302752966@qq.com')

            self.driver.find_element(By.XPATH, '//input[@type="radio" and @value="{}"]'.format(random.choice(['男', '女']))).click()
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_ddlProvince"]')).select_by_visible_text('湖北')
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_ddlCity"]')).select_by_visible_text('武汉')
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_lbObjectives"]')).deselect_all()
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_lbObjectives"]')).select_by_visible_text('通信技术')

            hobbies = random.sample(['音乐', '运动', '电影', '购物'], 3)
            for i in hobbies:
                self.driver.find_element(By.XPATH, '//label[text()="{}"]'.format(i)).click()

            self.SetElementValue('//*[@id="ctl00_mainContent_tbSelfAssement"]', '***' * 10)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_cbAcceptTerms"]').click()
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_btnSubmit"]').click()
            self.WaitElementDisappear('//*[@id="ctl00_mainContent_btnSubmit"]')
            self.driver.back()

            yield {'status': 'ok', 'message': '模拟表单提交成功'}

        sleep(1)
        self.driver.quit()

    @save_data('verifyCodeTest')
    def verifyCodeTest(self):
        """
        验证码测试
        """
        self.driver.get("https://captcha8.scrape.center/")

        for _ in range(10):

            self.InputElement('//form/div[1]//input', 'admin')
            self.InputElement('//form/div[2]//input', 'admin')
            self.InputElement('//form/div[3]//input', self.RecognizeCodeImg('//*[@id="captcha"]'))
            self.ClickElement('//span[text()="登录"]')

            try:
                self.driver.implicitly_wait(1)
                self.driver.find_element(By.ID, 'captcha').click()
                yield {'status': 'ok', 'message': '验证失败，尝试刷新...'}
            except:
                yield {'status': 'over', 'message': '登录成功...'}
                break
            finally:
                self.driver.implicitly_wait(30)

        self.driver.quit()

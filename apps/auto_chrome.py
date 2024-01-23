import uuid
import requests
from time import sleep
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

USER_DATA_DIR = Path.cwd().joinpath("XiaoMaRPA")


class AutoChrome:

    def __init__(self, mode):
        """
        构造函数
        """
        options = self.NewChromeOptions(mode)
        service = Service(executable_path="chromedriver.exe")

        self.driver = Chrome(options=options,
                             service=service,)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.actions = ActionChains(self.driver)

    def NewChromeOptions(self, mode) -> Options:
        """
        初始设置
        """
        options = Options()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-data-dir={USER_DATA_DIR.joinpath(str(uuid.uuid4()))}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        return options

    def WaitElementAppear(self, x_path):
        """
        等待元素出现
        """
        locator = (By.XPATH, x_path)
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located(locator))

    def WaitElementDisappear(self, x_path):
        """
        等待元素消失
        """
        locator = (By.XPATH, x_path)
        WebDriverWait(self.driver, 20).until_not(ec.invisibility_of_element_located(locator))

    def ClickElement(self, x_path, n=1):
        """
        元素点击
        """
        self.WaitElementAppear(x_path)
        element = self.driver.find_element(By.XPATH, x_path)
        self.actions.move_to_element(element).click(on_element=element).pause(n).perform()

    def InputElement(self, x_path, value):
        """
        元素输入
        """
        self.WaitElementAppear(x_path)
        element = self.driver.find_element(By.XPATH, x_path)
        element.clear()
        element.send_keys(value, Keys.ENTER)

    def SetElementValue(self, x_path, value):
        """
        设置元素文本
        """
        self.WaitElementAppear(x_path)
        element = self.driver.find_element(By.XPATH, x_path)
        self.driver.execute_script("arguments[0].focus();", element)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
        self.driver.execute_script("arguments[0].blur();", element)

    def RecognizeCodeImg(self, x_path):
        """
        识别验证码
        """
        self.WaitElementAppear(x_path)
        element = self.driver.find_element(By.XPATH, x_path)
        imgfile = element.screenshot_as_base64
        ocr_api = "https://api.rpacoder-my.cn/ocr/b64"
        response = requests.post(ocr_api, data=imgfile)

        return response.text

    def baiduTest(self):
        """
        百度测试
        """
        self.driver.get("https://www.baidu.com/")
        self.InputElement('//*[@id="kw"]', 'python')
        self.ClickElement('//*[@id="su"]')

        sleep(2)
        self.driver.quit()

    def formTest(self):
        """
        表单测试
        """
        self.driver.get("http://www.vrbrothers.com/cn/wqm/demo/pages/Demo-ComplexForm.aspx")

        for _ in range(20):

            self.SetElementValue('//*[@id="ctl00_mainContent_tbUsername"]', '用户名')
            self.SetElementValue('//*[@id="ctl00_mainContent_tbPassword"]', '123456')
            self.SetElementValue('//*[@id="ctl00_mainContent_tbEMail"]', '302752966@qq.com')

            self.driver.find_element(By.XPATH, '//input[@type="radio" and @value="{}"]'.format('男')).click()
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_ddlProvince"]')).select_by_visible_text('湖北')
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_ddlCity"]')).select_by_visible_text('荆州')
            Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_lbObjectives"]')).select_by_visible_text('通信技术')

            for i in '音乐,运动,电影,购物'.split(','):
                self.driver.find_element(By.XPATH, '//label[text()="{}"]'.format(i)).click()

            self.SetElementValue('//*[@id="ctl00_mainContent_tbSelfAssement"]', '***' * 10)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_cbAcceptTerms"]').click()
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_mainContent_btnSubmit"]').click()
            sleep(0.5)
            self.driver.back()

        sleep(0.5)
        self.driver.quit()

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
            except:
                break
            finally:
                self.driver.implicitly_wait(30)

        self.driver.quit()


class AutoWork(AutoChrome):

    def __init__(self, mode):
        super().__init__(mode)

    def process_task(self):
        """
        处理工作
        """
        pass

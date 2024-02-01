from time import sleep
from . import save_data
from .auto_chrome import AutoChrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class AutoWorking(AutoChrome):

    def __init__(self, mode, userdataDir=None):
        super().__init__(mode, userdataDir)

    def process(self):
        """
        新的流程
        """
        pass

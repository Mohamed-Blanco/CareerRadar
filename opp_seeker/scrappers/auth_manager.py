from selenium import webdriver

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from datetime import datetime, timedelta
import re
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from opp_seeker.scrappers.chromedriver_manager import Chromedriver_Manager


class Auth_Manager :
    def __init__(self,driver):
        self.driver =  driver
        self.USERNAME ="paypalabiad@gmail.com"
        self.PASSWORD = "labiad1234"

    def login_linkdein(self):
        try:
            self.driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")

            username_field.send_keys(self.USERNAME)
            password_field.send_keys(self.PASSWORD)

            password_field.send_keys(Keys.RETURN)
            logger.info("logged into the linkdein account ")
        except :
            logger.debug("Error when trying to login into the linkdein account ")


        return self.driver
    def login_indeed(self):
        pass



def main():
    ch = Chromedriver_Manager()
    drvr = ch.get_chrome_driver()
    au = Auth_Manager(drvr)
    au.login_linkdein()

if __name__ == "__main__" :
    main()
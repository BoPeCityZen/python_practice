# # 4 Feladat: charterbooker automatizálása


import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class TestFeladat1(object):
    def fill_form(self, mail: str):
        selector=Select(WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_totalGuests'))))
        selector.select_by_value('1')
        #btn1
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="next-btn next-btn1"]'))).click()
        #bf_date

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_date'))).send_keys('VALAMI')
        selector2 = Select(WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_time'))))
        selector2.select_by_value('Morning')
        selector3 = Select(WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_hours'))))
        selector3.select_by_value('3')
        # btn2
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="next-btn next-btn2"]'))).click()
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_fullname'))).send_keys('John Doo')
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_email'))).send_keys(mail)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.NAME, 'bf_message'))).send_keys('Nincs speciális kérés')
        #btn submit
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="submit-btn"]'))).click()

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/probavizsga/charterbooker.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    # * TC1: Ellenőrizd a helyes kitöltésre adott választ:
    # "Your message was sent successfully. Thanks! We'll be in touch as soon as we can, which is usually like lightning (Unless we're sailing or eating tacos!)."

    def test_c1(self):
        self.fill_form(mail="John@Doo.hu")
        exp_msg="Your message was sent successfully. Thanks! We'll be in touch as soon as we can, which is usually like lightning (Unless we're sailing or eating tacos!)."
        got_msg=WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//h2'))).text
        assert exp_msg == got_msg
        # print(got_msg)
        pass

    # * TC2: Készíts tesztesetet az e-mail cím validációjára.
    def test_c2(self):
        self.fill_form(mail="JohnDoohu")
        exp_msg='Please enter a valid email address.'
        got_msg = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'bf_email-error'))).text
        print(got_msg)
        print(exp_msg.upper())
        assert exp_msg.upper() == got_msg
        #bf_email-error

        pass


        # btn btn-primary




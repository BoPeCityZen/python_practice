# # 3 Feladat: Guess the number automatizálása


import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestFeladat1(object):
    def guess_and_tipp(self, new_guess: int):
        inp_field = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="input-group"]//input')))
        inp_field.clear()
        inp_field.send_keys(new_guess)
        guess_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-primary"]')))
        guess_btn.click()
        check_tipp = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//p[@class="alert alert-warning"]'))).text
        return check_tipp

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/probavizsga/guess_the_number.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    # ## TC1
    # __TC1__: Egy tesztet kell írnod, ami addig találgat a megadott intervallumon belül, amíg ki nem találja a helyes számot.

    def test_c1(self):
        low_end=0
        high_end=100
        new_guess=50
        check_tipp = self.guess_and_tipp(int(new_guess))
        # inp_field=WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="input-group"]//input')))
        # inp_field.send_keys(new_guess)
        # guess_btn= WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-primary"]')))
        # guess_btn.click()
        # check_tipp=WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_element_located((By.XPATH, '//p[@class="alert alert-warning"]'))).text
        # print(check_tipp)

        while check_tipp == 'Yes! That is it.':
            if check_tipp == 'Guess higher.':
                low_end=new_guess
                new_guess=random.randint(new_guess,high_end)
                print(new_guess)
            elif check_tipp == 'Guess lower.':
                high_end = new_guess
                new_guess = random.randint(new_guess, low_end)
                print(new_guess)

            check_tipp = self.guess_and_tipp(int(new_guess))

            # inp_field.send_keys(new_guess)
            # guess_btn.click()
            # assert check_tipp == 'Yes! That is it.'

    def test_c2(self):

        new_guess = -19
        check_tipp = self.guess_and_tipp(int(new_guess))
        print(check_tipp)
        assert check_tipp == 'Guess higher.'

        new_guess = 255
        check_tipp = self.guess_and_tipp(int(new_guess))
        print(check_tipp)
        assert check_tipp == 'Guess lower.'


        # btn btn-primary




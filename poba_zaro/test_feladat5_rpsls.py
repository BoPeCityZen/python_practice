# # 5 Feladat: Rock, Paper, Scissors, Lizard, Spock


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
   

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/probavizsga/rpsls.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    # ## TC01: Elindítás előtti ellenőrzés
    #
    # * Ellenőrizd le, hogy az oldal betöltésekor, középen megjelennek-e a `Rock, Paper, Scissors, Lizard, Spock` feliratok.

    def test_c1(self):
        selection=WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//button//span')))

        elements=['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        for i in range(len(elements)):
            # print(selection[i].text)
            assert selection[i].text == elements[i]
        pass


    ## TC02: Körök ellenőrzése    #
    # - Ellenőrizd le, hogy a középen lévő `Rock` megnyomása után, megjelenik-e baloldalt a `Rock` icon.
    # - Ezután azt is ellenőrizd le, hogy a középen lévő `Lizard` megnyomása után, megjelenik-e baloldalt a `Lizard` icon.
    def test_c2(self):
        #rock
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'rock'))).click()

        #history-item win
        history_items=WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div//i')))
        got_classname=history_items[1].get_attribute('className')
        assert got_classname=='fa fa-hand-rock-o'
        pass

    ## TC03: New class    #
    # - Ellenőrizd le, hogy a középen lévő `Rock` a megnyomása után kap-e egy extra class-t, aminek az értéke vagy `win` vagy `loss`.

    def test_c3(self):
        #rock
        rock_btn=WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'rock')))
        rock_btn.click()
        used_btn_class=['win','lose','tie']
        got_classname=rock_btn.get_attribute('className')
        print(got_classname)
        print (got_classname in used_btn_class)
        assert got_classname in used_btn_class
        pass


        # btn btn-primary




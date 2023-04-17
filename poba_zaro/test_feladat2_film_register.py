# # 2 Feladat: Film register applikáció funkcióinak automatizálása


import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestFeladat1(object):

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/probavizsga/film_register.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    # ## TC1
    # Teszteld le, hogy betöltés után megjelennek filmek az alkalmazásban, méghozzá 24 db.
    def test_filmlista(self):
        filmek = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="container-movies"]')))
        # print(len(filmek))
        assert len(filmek) == 24

    def test_ujfilm(self):
        filmekB = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="container-movies"]')))
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="mostra-container-cadastro"]'))).click()

        Film = {'title': 'Black widow',
                'Release year': '2021',
                'Chronological year of events': '2020',
                'Trailer url': 'https://www.youtube.com/watch?v=Fp9pNPdNwjI',
                'Image url': 'https://m.media-amazon.com/images/I/914MHuDfMSL._AC_UY327_FMwebp_QL65_.jpg',
                'Film summary': 'https://www.imdb.com/title/tt3480822/'
                }

        inp_fields=WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="container-cadastro center ativo"]//input')))
        # use_this=inp_fields[0]
        time.sleep(1)
        # use_this.send_keys('Valami')
        i=0
        for pairs in Film.items():
            inpName = inp_fields[i]
            send_this_key = pairs[1]
            # print(f'inp Name & value: {inpName}, {send_this_key}')
            inpName.send_keys(send_this_key)
            i+=1
        save_btn=WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH, '//button[@onclick="salvarFilme()"]')))
        save_btn.click()
        filmekA = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="container-movies"]')))
        assert len(filmekA) == len(filmekB) + 1

        #
        # Az ellenőrzésekhez használj `pytest` keretrendszert. A tesztjeidben mindenképp `assert` összehasonlításokat használj!


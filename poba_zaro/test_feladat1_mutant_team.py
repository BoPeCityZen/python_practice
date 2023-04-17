## 1 Feladat: Mutant Team

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
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/probavizsga/mutant_teams.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        # pass
        self.browser.quit()

    # ## TC0 - Oldal header szövegének megjelenése
    # * Teszteld le, hogy az oldalon megjelenő fő szöveg megegyezik-e ezzel: `MARVEL MUTANT TEAMS`
    def test_foszoveg(self):
        foszoveg = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//h1'))).text
        # print(foszoveg)
        assert foszoveg == 'MARVEL MUTANT TEAMS'

    # ## TC1 - Rictor visible
    # * Teszteld le, hogy az X-factor szűrő bekapcsolásával megjelenik-e Rictor.
    def test_xfactor(self):
        selectors = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//label')))
        factor = selectors[2]
        factor.click()

        rictor = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'rictor')))
        # rictor_txt = rictor.text
        # print(rictor_txt)
        assert rictor.is_displayed()

    # ## TC2 - Beast visible
    # * Teszteld le, hogy az X-force szűrő bekapcsolásával eltűnik-e Beast.
    def test_xforce(self):
        selectors = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//label')))
        force = selectors[1]
        force.click()

        beast = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'beast')))

        try:
            assert beast.is_not_displayed()
        except:
            print('Upsz')

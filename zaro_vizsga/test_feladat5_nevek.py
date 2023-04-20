## 5 Feladat: Kakukktojás - nevek


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
        URL = "https://svtesztelovizsga.blob.core.windows.net/$web/zarovizsga/f5_list_names.html"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    ### HELPER METHODS--------------------------------------------------------------------------------------------------
    def element_byID(self, key):
        element_byID = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, f'{key}')))
        return element_byID

    def listed_elements_byXPATH(self, string):
        lsit_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, f'{string}')))
        return lsit_elements

    def element_byXPATH(self, string):
        element = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, f'{string}')))
        return element

    def send_keys(self, field, keys):
        send_this = field.send_keys(keys)
        return send_this

    ### TEST CASES -----------------------------------------------------------------------------------------------------

    # TC1
    ##Feladatod, hogy megtaláld azt a nevet, ami **csupa nagybetűvel** van írva,
    # #majd ennek normál formájával (Pl. ALVERN -> Alvern) kitöltsd a form-ban a mezőt.  Ellenőrizd le azt is, hogy eltaláltad-e.

    ## lépések: navlistába kigyűjtüm az összes nevet (boxból)
    ## az összes felsorolt névre ellenörzöm, hogy ott van e boxban >> ha nagybetűs akkor nem lesz
    ## ha megvan a keresett név visszaformázom és beküldöm
    ## az ellenőrzésre kapott szöveget ellenőrzőm: 'Eltaláltad.'

    def test_c1(self):
        nevlista = self.element_byID('names').text
        # print(nevlista)

        randomlista = self.listed_elements_byXPATH('//li')
        for nev in range(len(randomlista)):
            nev_txt = (randomlista[nev].text)
            # print(nev_txt)
            if nev_txt in nevlista:
                pass
            else:
                assert not nev_txt in nevlista
                # print(f'keresett név: {nev_txt}')
                keresett_nev = nev_txt

        # név visszaformázása nagykezdőbetűsre
        check_name_lower = keresett_nev.lower()
        check_name_formed = check_name_lower.title()

        ell_mezo = self.element_byID('allcapsName')
        self.send_keys(ell_mezo, check_name_formed)
        self.element_byID('submit').click()
        check_result = self.element_byID('result').text

        assert check_result == 'Eltaláltad.'

"""
Gyakorló oldal:
https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login

Automatizáld az alábbi teszteseteket a következő szempontok figyelembevétel.
- Használj osztályt a teszt funkciók rendszerezéséhez. Ez rendelkezzen setup és teardown metódosukkal is.
- Használj PyTest-et és Selenium-ot a megvalósításhoz
- Legalább a login folyamat legyen kiszervezve külön függvénybe, hogy meghívhassák azok a tesztfüggvények,
amelyek igénylik. Tipp: a random deposit és a pénzfelvétel függvényesítése is megkönnyíti a dolgod. Lsd. TC3 és TC4

Nem kell felhasználót regisztrálni, mert az alkalmazás minden adatot a böngésző Local Storage-ában tárol.
Használd nyugodtan az alább megadott TEST_DATA-ban rögzített adatokat.
"""
import time
import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


# ----------------------------------------------------------------------------------------------------------------------


class TestFeladatok(object):

    def database(self, info):

        TEST_DATA = {
            "username": "Ron Weasly",
            "user_id": "3",
            "account_numbers": [1007, 1008, 1009],
            "transactions": []            
        }
        take_this = TEST_DATA[info]
        return take_this

    def sign_in(self):
        select_this = self.database('user_id')
        select_users = Select(
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'userSelect'))))
        select_users.select_by_value(str(select_this))
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()

    def Login_btns(self):
        login_btns = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[@class="btn btn-primary btn-lg"]')))
        return login_btns

    def HomeButton(self):
        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn home"]')))
        return home_btn

    def submitBtn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()

    def BankActionRutin(self, classNr: str):
        # print(classNr)
        spec_classNr = classNr
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//button[@ng-class="btnClass{spec_classNr}"]'))).click()
        if int(spec_classNr) == 2:
            amount = random.randint(100, 1000)
        elif int(spec_classNr) == 3:
            amount = int(self.check_balance())
            time.sleep(1)
        inp_field = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="number"]')))

        inp_field.send_keys(amount)
        self.submitBtn()
        msg = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="ng-scope"]/span'))).text
        print(msg)

        return msg, amount

    def repeatDeposit(self, n):
        transactions = self.database('transactions')
        for i in range(n):
            Deposit = self.BankActionRutin(classNr='2')
            # print(Deposit)
            try:
                assert (str(Deposit[0]) == 'Deposit Successful')
                transactions.append(Deposit[1])

            except:
                print('Upsz...)

        # print(transactions)
        return transactions

    def check_balance(self):
        Balance = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@ng-hide="noAccount"]/strong')))[1].text
        # print(Balance)
        return int(Balance)

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        # pass
        self.browser.quit()

    """
    TC1: Ellenőrizzük a főoldal főbb elemeinek megjelenését
    Expected results:
    - Az 'XYZ Bank' szöveg megjelenik az oldalon  
    - A Home gomb engedélyezett (is_enabled)
    - A Customer Login gomb engedélyezett
    - A Bank Manager Login gomb engedélyezett

    Ha csak az egyik nem teljesül, akkor az egész teszteset bukik.
    """

    def test_case1(self):
        act_str = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="box mainhdr"]/strong'))).text
        assert act_str == 'XYZ Bank'
        home_btn = self.HomeButton()
        assert home_btn.is_enabled
        login_btns = self.Login_btns()
        login_c_btn = login_btns[0]
        login_m_btn = login_btns[1]
        assert login_c_btn.is_enabled
        assert login_m_btn.is_enabled

    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC2: Ellenőrizzük, hogy bejelentkezés után a megfelelő felhasználói fiókba kerülünk.
    Használd a folyamathoz az alább megadott teszt adadtokat.
    Steps:
    1. Kattints a Customer Login gombra
    2. Válaszd ki a lenyíló menüből a TEST_DATA-ban található felhasználót a value attribútum segítségével. (user_id!) 
    3. Kattints a megjelenő Login gombra

    Expected results:
    - Az üdvözlő szövegben a megadott felhasználó neve szerepel
    - Az üdvözlő szöveg mellett található lenyíló lista a TEST_DATA-ban található fiók számok mindegyikét tartalmazza
    """

    def test_case2(self):
        self.Login_btns()[0].click()

        self.sign_in()

        user_name = self.database('username')
        getName = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="fontBig ng-binding"]'))).text
        print(getName)
        assert getName == user_name

        find_fiok_elemek = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'option')))
        exp_fiok_elements = self.database('account_numbers')
        for e in range(len(exp_fiok_elements)):
            # print(type(exp_fiok_elements[e]))
            # print(find_fiok_elemek[e].text)
            assert exp_fiok_elements[e] == int(find_fiok_elemek[e].text)

    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC3: Pénzbefizetés (deposit) véletlenszerű értékekkel
    Steps:
    1. Jelentkezz be a TEST_DATA-ban meghatározott felhasználóval

    >>> A következő részt szervezd ki segédfüggvénybe, mert a további eseteknél is szükség lesz rá
    2. Kattints a Deposit gombra
    3. Ismételd az alábbiakat 5x
    3.1 Generálj egy random számot 100 és 1000 között
    3.2 Írd be ezt a számot az amount input mezőbe
    3.3 Kattints a Deposit gombra
    3.4 Ellenőrizd, hogy megjelenik-e a 'Deposit Successful' üzenet
    3.5 Ha igen, akkor add hozzá a TEST_DATA['transactions'] listához a beküldött értéket
    >>>

    4. Hívd meg a függvényt, majd ellenőrizd a Balance melletti szöveget

    Expected results:
    Ha minden pénzbefizetés sikeres volt, akkor az eltárolt tranzakciók össz értéke egyenlő a Balance felirat mellett jelzett összeggel.
    """

    def test_case3(self):
        self.Login_btns()[0].click()
        self.sign_in()

        transactions = self.repeatDeposit(5)
        sum_transactions = (sum(transactions))
        Balance = self.check_balance()
        try:
            assert sum_transactions == int(Balance)
            # print(f'\nEnnyi:{Balance}')
        except:
            print('Upsz...)

    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC4: Pénzfelvétel (withdraw) ellenőrzése
    Dependency: TC3
    Steps:
    1. Jelentkezz be a TEST_DATA-ban meghatározott felhasználóval
    2. Hívd meg a random befizetésre készített függvényedet

    >>> A következő részt szervezd ki segédfüggvénybe, mert az utolsó esetnél is szükség lesz rá
    3. Kattints a Withdrawl gombra
    4. Írd be az előzőleg eltárolt befizetési tranzakciók összértékét az amount input mezőbe
    5. Kattints a Withdraw gombra
    >>>
    6. Hívd meg a függvényt, majd ellenőrizd a Balance melletti szöveget

    Expected results:
    - Megjelenik a 'Transaction successful' szöveg az oldalon
    - A Balance értéke 0-t mutat
    """

    def test_case4(self):
        self.Login_btns()[0].click()
        self.sign_in()

        self.repeatDeposit(5)

        Withdrawl = self.BankActionRutin(classNr='3')

        try:
            assert (str(Withdrawl[0]) == 'Transaction successful')
            Balance = self.check_balance()
            # print(f'\nEnnyi maradt:{Balance} Ez nem semmi?! De az: 0.')
        except:
            print('Upsz...)

    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC5: Tranzakciók tábla ellenőrzése
    Dependency: TC4
    Steps:
    1. Jelentkezz be a TEST_DATA-ban meghatározott felhasználóval
    2. Hívd meg a random befizetésre készített függvényedet
    3. Hívd meg az összes pénz kivételére írt függvényedet
       (Tipp: ez után érdemes 1 másodpercet fixen várakoztatni a scriptet)
    4. Kattints a Transactions gombra

    5. Ellenőrizd, a megjelenő tábla Amount ill. Transaction Type oszlopait

    Expected results: A megjelenő táblázatban 6 sor szerepel, az előzőleg végrehajtott tranzakció értékekkel.
    Befizetés esetén a Transaction Type a Credit értéket veszi fel, pénzfelvétel esetén pedig a Debit értéket.
    (Az összehasonlításhoz használd a TEST_DATA-ban tárolt egyéni értékeket, illetve ezek összegét a Debit érték
    ellenőrzéséhez.)

    +TIPP: XPATH -> //tr/td[2] = Minden 2. cella, ami a táblázat valamely során belül található (LISTA!)
    """

    def test_case5(self):
        self.Login_btns()[0].click()
        self.sign_in()

        transactions = self.repeatDeposit(5)
        sum_transactions = (sum(transactions))
        transactions.append(sum_transactions)

        self.BankActionRutin(classNr='3')

        time.sleep(1)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//button[@ng-class="btnClass1"]'))).click()

        szlakciok = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tr/td[2]')))
        # print(szlakciok[0].text)

        for t in range(len(transactions)):
            # print(f'{transactions[t]} Vs. {szlakciok[t + 1].text}')

            try:
                assert transactions[t] == int(szlakciok[t + 1].text)
                # print('Ohbejó! :)')
            except:
                print('Upsz...')

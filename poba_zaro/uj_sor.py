"""
Gyakorló oldal:
https://www.saucedemo.com/

Automatizáld az alábbi teszteseteket a következő szempontok figyelembevétel.
- Használj osztályt a teszt funkciók rendszerezéséhez. Ez rendelkezzen setup és teardown metódosukkal is.
Tipp: Használd a rendelkezésedre álló template-et a kiinduláshoz.
- Használj PyTest-et és Selenium-ot a megvalósításhoz
- A login folyamat legyen kiszervezve külön függvénybe.
Tipp: használj paramétereket (user,password), hogy szükség esetén könnyen át tudd adni
a USER dictionary-ben definiált felhasználónév-jelszó párosokat
"""





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
        URL = "https://www.saucedemo.com/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    def use_this(self, u, p):
        inp_fields = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="form_group"]//input')))
        USER = {
            1: {'standard': 'standard_user', },
            2: {'locked_out': 'locked_out_user', },
            3: {'password': 'secret_sauce', },
        }
        for pairs in USER[u].items():
            inpfield_username = inp_fields[0]
            send_username = pairs[1]

        for pairs in USER[p].items():
            inpfield_passworld = inp_fields[1]
            send_password = pairs[1]
        print(f'inp Name & pass:\n {inpfield_username} >> {send_username}'
                  f'\n {inpfield_passworld} >> {send_password}')
        inpfield_username.send_keys(send_username)
        inpfield_passworld.send_keys(send_password)
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'login-button'))).click()



    """
    TC1: Ellenőrizzük, hogy megfelelő hibaüzenet jelenik-e meg, ha a kizárt felhasználóval akarunk belépni az oldalra.
    Expected results:
    A locked_out_user-el történő belépési kísérlet után az 'Epic sadface: Sorry, this user has been locked out.'
    tartalmú hibaüzenet olvasható a képernyőn.
    """
    def test_c1(self):

        self.use_this(2,3)
        check_this='Epic sadface: Sorry, this user has been locked out.'
        got_msg = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//h3'))).text
        print(got_msg)
        assert check_this == got_msg
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------

    """
    TC2: Ellenőrizzük a termék lista rendezésére szolgáló lenyíló elem választási lehetőségeinek számát.
    Steps:
    1. Belépés standard_user-el
    2. Megfelelő select lekérése 
    3. A benne található optionok megszámlálása
    
    Expected results: a lenyíló elem 4 elemet tartalmaz összesen
    """
    def test_c2(self):

        self.use_this(1,3)
        drop_dwn=WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//select/option')))
        mnu_tagsNR=(len(drop_dwn))
        assert mnu_tagsNR == 4



    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC3: Ellenőrizzük a kosár számláló működését
    Steps:
    1. Belépés standard_user-el
    2. Kérjük le az első 3 ADD TO CART FELIRATÚ GOMBOT
    3. Kattintsunk mindegyik gombra egyszer
    
    Expected results: A jobb felső sarokban lévő kosáron megjelenő számláló 3-at mutat
    """

    def test_c3(self):

        self.use_this(1, 3)
        #inv_item_lst=[]
        for i in range(3):
            new_btn=WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn_primary btn_small btn_inventory"]')))
            print(new_btn.text)
            assert new_btn.text=='Add to cart'
            #inv_item_lst.append(new_btn)
            new_btn.click()
        ennyi = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="shopping_cart_badge"]'))).text
        assert ennyi == '3'



            # ----------------------------------------------------------------------------------------------------------------------

    """
    TC4: Ellenőrizzük a megjelenő árak valuta típusát
    Steps:
    1. Belépés standard_user-el
    2. Kérjük le az összes ár szöveget az oldalról
    3. Egyenként ellenőrizzük, hogy a $ jel szerepel-e bennük
    
    Expected results: Minden ár megjelölés $ jellel kezdődik.
    """

    def test_tc4(self):
        self.use_this(1,3)
        price_list=WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="inventory_item_price"]')))
        for p in range(len(price_list)):
            price=price_list[p].text
            print(price_list[p].text)
            assert '$' in price
            assert '$' == price[0]


    # ----------------------------------------------------------------------------------------------------------------------

    """
    TC5: Megjelenített képek ellenőrzése
    Steps:
    1. Belépés standard_user-el
    2. Kérjük le az első áru képének src attribútumát
    3. Kattintsunk rá a képre
    4. A megjelenő részletező oldalon kérjük le a kép src attribútumát
    
    Expected results: A két kép src attribútuma megegyezik. (Ugyanazt a képet jeleníti meg az oldal)
    +Vigyázat: A lista oldalon a képek class-a ugyanaz, mint a szülő div-eknek!
    """
    def test_tc5(self):
        self.use_this(1,3)
        imgs=WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//img[@class="inventory_item_img"]')))
        print(imgs)
        first_img=imgs[0]
        listed_img_url=first_img.get_attribute("src")
        print(listed_img_url)
        first_img.click()
        img=WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="inventory_details_img"]')))
        img_url=img.get_attribute("src")
        print(img_url)
        assert listed_img_url==img_url



# ----------------------------------------------------------------------------------------------------------------------
# NEHEZEBB FELADAT, CSAK HA ÉRZED HOZZÁ A CSÍ-T :)
"""
TC6: Megfordított ABC sorrend szerinti listázás helyességének ellenőrzése
Steps:
1. Belépés standard_user-el
2. Kérjük le az összes termékmegnevezést és tároljuk el őket egy fordítottan rendezett listában
3. A rendezésre szolgáló lenyíló elemben válasszuk a Name (Z to A) lehetőséget
4. Kérjük le újra az összes termékmegnevezést egy új listába

Expected results: a rendezés előtti- és utáni listáknak meg kell egyezniük."""
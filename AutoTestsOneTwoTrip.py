from selenium import webdriver
from unittest import TestCase
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RightWork(TestCase):

    def setUp(self):
        """
        Предусловия:
        1.  Зайти на сайт www.onetwotrip.com
        """
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.onetwotrip.com/")

        self.wait = WebDriverWait(self.driver, 10)


    def test_WrongCities(self):
        """
         Шаги :
         1. Выбрать тип рейса "В одну сторону"
         2. В полях "Откуда" и "Куда" выставить одинаковые города
         3. В поле "Когда" выставить любую дату
         4. Нажать кнопку "Найти"

         Проверка:
         Появляется сообщение "Неверно задан маршрут. Совпадают пункты вылета и прилёта."
         """
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.searchFormABWayControlItem:nth-child(3)'))).click()

        elem = self.driver.find_element_by_css_selector('#from0')
        elem.send_keys('Новосибирск')
        elem = self.driver.find_element_by_css_selector('#to0')
        elem.send_keys('Новосибирск')

        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[7]/div/div[2]")))
        elem.click()

        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.searchFormABSubmit'))).click()

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".comment > p:nth-child(1)")))
        self.assertEqual(elem.text, "Неверно задан маршрут. Совпадают пункты вылета и прилёта.")

    def test_WrongDates(self):
        """
            Шаги :
            1. Выбрать тип рейса "Туда и обратно"
            2. В полях "Откуда" и "Куда" выставить разные города
            3. В поле "Туда" выставить любую дату
            4. В поле "Обратно" выбрать дату, раньше даты в поле "Туда"
            5. Нажать кнопку "Найти"

            Проверка:
            Появляется сообщение "Неверно заданы даты"
            """
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.searchFormABWayControlItem:nth-child(2)'))).click()

        elem = self.driver.find_element_by_css_selector('#from0')
        elem.send_keys('Новосибирск')
        elem = self.driver.find_element_by_css_selector('#to0')
        elem.send_keys('Екатеринбург')

        elem = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[12]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[4]/td[6]/div/div[2]")))
        elem.click()

        elem = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="date1"]')))
        elem.click()
        elem = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[12]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[7]/div/div[2]")))
        elem.click()

        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.searchFormABSubmit'))).click()

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".comment > p:nth-child(1)")))
        self.assertEqual(elem.text, "Неверно заданы даты")


    def test_Autorization(self):
        """
            Шаги :
            1. Открыть "Личный кабинет"
            2. Нажать на логотип Twitter
            3. В открывшемся окне ввести данные от аккаунта Twitter

            Проверка:
            Поле "Личный кабинет" замениться на идентификаторы пользователя из выбранной соц. сети
            """
        self.driver.find_element_by_css_selector('.enter').click()

        elem = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="SocialAuth"]/div[2]/ul/li[2]/a')))
        elem.click()

        self.driver.switch_to_window(self.driver.window_handles[1])
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username_or_email')))
        elem.send_keys('fedosovdn@mail.ru')
        elem = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
        elem.send_keys('ltdrbcexrb')
        elem = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#allow')))
        elem.click()

        self.driver.switch_to_window(self.driver.window_handles[0])
        self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "myprofile"), "fedosov0405"))


    def test_WrongRegistration(self):
        """
            Шаги :
            1. Открыть "Личный кабинет"
            2. В поле "Электронная почта" ввести почту
            3. Ввести пароль в соответствующее поле
            4. Ввести отличный пароль от введенного ранее в поле "Повторить пароль"
            5. Нажать кнопку "Зарегистрироваться"

            Проверка:
            Окно регистрации активно(регистрация не прошла)
            """
        self.driver.find_element_by_css_selector('.enter').click()

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_reg_email')))
        elem.send_keys('fedosovdn@mail.ru')

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_reg_pas')))
        elem.send_keys('bla_bla')

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_confirmreg_pas')))
        elem.send_keys('bla_bla_bla')

        elem.send_keys(Keys.TAB, Keys.ENTER)

        self.assertTrue(self.driver.find_element_by_xpath('//*[@id="SocialRegAuth"]').is_displayed())


    def test_baby(self):
        """
            Шаги :
            1. Выбрать тип рейса "В одну сторону"
            2. В полях "Откуда" и "Куда" выставить разные города
            3. В поле "Когда" выставить любую дату
            4. Нажать кнопку "Найти"
            5. Открыть первый вариант рейса
	    6. Вводим информацию пассажира (дата рожения: 04.04.2016)
	    7. Нажать кнопку "Перейти"

            Проверка:
            Появляется сообщение "Количество младенцев в брони не должно превышать количество взрослых."
            """
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.searchFormABWayControlItem:nth-child(3)'))).click()

        elem = self.driver.find_element_by_css_selector('#from0')
        elem.send_keys('Новосибирск')
        elem = self.driver.find_element_by_css_selector('#to0')
        elem.send_keys('Екатеринбург')

        elem = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[12]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[4]/td[6]/div/div[2]")))
        elem.click()

        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.searchFormABSubmit'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FirstPrefered"]/div/div/div[3]/button'))).click()

        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_avia_book_email')))
        elem.send_keys('fed@mail.ru')
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_lastName0')))
        elem.send_keys('dan')
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_firstName0')))
        elem.send_keys('ssa ada')
        elem.send_keys(Keys.TAB, Keys.NUMPAD0, Keys.NUMPAD4, Keys.NUMPAD0, Keys.NUMPAD4, Keys.NUMPAD2, Keys.NUMPAD0, Keys.NUMPAD1, Keys.NUMPAD6)
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_passNumber0')))
        elem.send_keys('2987545856')
        elem.send_keys(Keys.TAB, Keys.ENTER)
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".comment > p:nth-child(1)")))
        self.assertEqual(elem.text,"Количество младенцев в брони не должно превышать количество взрослых.")



    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

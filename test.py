from unittest import TestCase
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class OttripTest(TestCase):
    def setUp(self):
        """
        Предусловие:
        зайти на сайт www.onetwotrip.com
        нажать "личный кабинет"
        """
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.driver.get("http://www.onetwotrip.com/ru")
        self.driver.find_element_by_class_name("enter").click()

    def tearDown(self):
        self.driver.quit()

    def test_forgot_password_non_existent_email(self):
        """
        Тест-кейс "Проверка вывода сообщения об ошибке при вводе несуществующего email в форме "забыли пароль""
        Шаги:
        1. Зайти на сайт "www.onetwotrip.com"
        2. Нажать "Личный кабинет"
        3. В открывшемся окне нажимаем "забыли пароль"
        4. В открывшемся окне ввести несуществующий email
        Ожидание:
        Вывод сообщения об ошибке "Пользователя с таким email не существует" в браузере.
        """
        driver = self.driver
        driver.find_element_by_class_name("getNewPas").click()
        driver.find_element_by_id("input_remind_email").send_keys("llllll@mail.ru")

        button = driver.find_element_by_css_selector(
            "table.layout:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > button:nth-child(1)")
        button.click()

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#RemindAuth > div:nth-child(3)")))

        error = driver.find_element_by_css_selector("#RemindAuth > div:nth-child(3)").text
        self.assertIn("Пользователя с таким email не существует", error)

    def test_forgot_password_correct_email(self):
        """
        Тест-кейс "Проверка вывода сообщения об отправке нового пароля на указанный email в форме "забыли пароль""
        Шаги:
        1.Нажать "забыли пароль"
        2.В поле "Электронная почта" ввести зарегистрированный на onetwotrip email
        3.Нажать кнопку "Получить пароль"
        Ожидание:
        Вывод сообщения об отправке нового пароля на указанный email.
        """
        driver = self.driver
        driver.find_element_by_class_name("getNewPas").click()
        driver.find_element_by_id("input_remind_email").send_keys("ld040994@mail.ru")

        button = driver.find_element_by_css_selector(
            "table.layout:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > button:nth-child(1)")
        button.click()

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,"smallText")))

        message = driver.find_element_by_class_name("smallText")
        self.assertTrue(message.is_displayed())

    def test_auth_incorrect_login(self):
        """
        Тест-кейс "Проверка вывода сообщения об ошибке при вводе неверного логина в форме авторизации"
        Шаги:
        1.В поле "Электронная почта" вести почту незарегистрированную на onetwotrip
        2.В поле "Пароль" ввести пароль
        3.Нажать кнопку "Войти"
        Ожидание:
        Вывод сообщения "Неправильный пароль или почта"
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys("l040994@mail.ru")
        driver.find_element_by_id("input_auth_pas").send_keys("040994alex")
        driver.find_element_by_class_name("pos_but").click()

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,"Error")))

        error = driver.find_element_by_class_name("Error").text
        self.assertIn("Неправильный пароль или почта",error)

    def test_auth_correct(self):
        """
        Тест-кейс "Проверка ввода верного логина и пароля в форме авторизации"
        Шаги:
        1.В поле "Электронная почта" вести почту зарегистрированную на onetwotrip
        2.В поле "Пароль" ввести верный пароль
        3.Нажать кнопку "Войти"
        Ожидание:
        Успешная авторизация (название кнопки личный кабинет заменяется на email адрес)
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys("ld040994@mail.ru")
        driver.find_element_by_id("input_auth_pas").send_keys("040994alex")
        driver.find_element_by_class_name("pos_but").click()

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,"myprofile")))

        profile = driver.find_element_by_class_name("myprofile")
        self.assertEqual(profile.text,"ld040994@mail.ru")

    def test_auth_facebook(self):
        """
        Тест-кейс "Проверка ввода верного логина и пароля в форме авторизации"
        Шаги:
        1.Нажать на иконку Facebook
        2.В новом окне ввести логин и пароль от аккаунта Facebook
        3.Нажать кнопку "Войти"
        Ожидание:
        Успешная авторизация (название кнопки "личный кабинет" заменяется название профиля)
        """
        driver = self.driver
        driver.find_element_by_css_selector(".sLinks_inside > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)").click()
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element_by_id("email").send_keys("alexld45@mail.ru")
        driver.find_element_by_id("pass").send_keys("040994alex")
        driver.find_element_by_id("loginbutton").click()
        driver.switch_to.window(driver.window_handles[0])

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,"myprofile")))

        profile = driver.find_element_by_class_name("myprofile")
        self.assertEqual(profile.text,"Алексей Демин")

if __name__ == '__main__':
    unittest.main()
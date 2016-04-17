from unittest import TestCase
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class OttripTest(TestCase):
    def setUp(self):
        """
        Предусловие:
        зайти на сайт www.onetwotrip.com
        нажать "личный кабинет"
        """
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get("http://www.onetwotrip.com/ru")
        self.driver.find_element_by_class_name("enter").click()

    def test_forgot_password_non_existentEmail(self):
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
        error = driver.find_element_by_css_selector("#RemindAuth > div:nth-child(3)").text
        self.assertIn("Пользователя с таким email не существует", error)
        driver.quit()

    def test_forgot_password_correctEmail(self):
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
        self.assertTrue(driver.find_element_by_class_name("smallText").is_displayed())
        driver.quit()

    def test_auth_incorrectLogin(self):
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
        error = driver.find_element_by_class_name("Error").text
        self.assertIn("Неправильный пароль или почта",error)
        driver.quit()

    def test_auth_correctLoginAndPass(self):
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
        profile = driver.find_element_by_class_name("myprofile")
        self.assertEqual(profile.text,"ld040994@mail.ru")
        driver.quit()

    def test_auth_Facebook(self):
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
        profile = driver.find_element_by_class_name("myprofile")
        self.assertEqual(profile.text,"Алексей Демин")
        driver.quit()

    def TearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
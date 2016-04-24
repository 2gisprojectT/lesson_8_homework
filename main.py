import time
import unittest
from threading import Thread
from unittest import TestCase
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestGmailAuth(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://mail.google.com/")
        self.driver.implicitly_wait(5)

    def wait_captcha_img(self, driver):
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'captcha-box'))
        )
    def test_email_captcha(self):
        """
        Название : Проверка появления поля капчи при вводе e-mail

        Шаги :
        1.Вводим неверные e-mail и подтверждаем ввод пока не появиться поле капчи

        Тест пройден:
        Появляется поле ввода капчи

        """
        driver = self.driver
        email = driver.find_element_by_name("Email")
        email.send_keys("sndb11")
        captcha = self.driver.find_element_by_id("captcha-img")
        t1 = Thread(target=self.wait_captcha_img, args=(driver,))
        t1.start()
        while (not captcha.is_displayed()):
            email.send_keys("a")
            email.submit()
    def test_not_register_email(self):
        """
            Название : Проверка появления сообщения: Не удалось распознать адрес электронной почты.

            Шаги :
            1.Вводим не существующий e-mail
            2.Подтверждаем ввод

            Тест пройден:
            Появляется сообщение : Не удалось распознать адрес электронной почты.

            """
        driver = self.driver
        email = driver.find_element_by_name("Email")
        email.send_keys("sndb11")
        email.submit()
        error = driver.find_element_by_css_selector(".has-error .error-msg")
        self.assertEqual(error.text, "Не удалось распознать адрес электронной почты.")

    def test_not_valid_email(self):
        """
            Название : Проверка появления сообщения: "Введите адрес электронной почты."

            Шаги :
            1.Вводим не e-mail
            2.Подтверждаем ввод

            Тест пройден:
            Появляется сообщение : "Введите адрес электронной почты."

            """
        driver = self.driver
        email = driver.find_element_by_name("Email")
        email.send_keys("sndb11@")
        email.submit()
        error = driver.find_element_by_css_selector(".has-error .error-msg").text
        self.assertEqual(error, "Введите адрес электронной почты.")

    def test_long_email(self):
        """
            Название : Проверка ввода e-mail'а превыщающего допустимую длинну"

            Шаги :
            1.Вводим e-mail больше 200 знаков
            2.Подтверждаем ввод

            Тест пройден:
            Появляется сообщение : "Слишком длинный адрес электронной почты."

            """
        driver = self.driver
        email = driver.find_element_by_name("Email")
        key = "a" * 201
        email.send_keys(key)
        email.submit()
        error = driver.find_element_by_css_selector(".has-error .error-msg").text
        self.assertEqual(error, "Слишком длинный адрес электронной почты.")

    def test_long_passwd(self):
        """
            Название : Проверка ввода пароля превыщающего допустимую длинну"

            Шаги :
            1.Вводим пароля больше 200 знаков
            2.Подтверждаем ввод

            Тест пройден:
            Появляется сообщение : "Должно быть не более 200 символов"

            """
        driver = self.driver
        email = driver.find_element_by_name("Email")
        email.send_keys("doctorvra4@gmail.com")
        email.submit()
        key = "a" * 201
        passwd = self.driver.find_element_by_name("Passwd")
        passwd.send_keys(key)
        passwd.submit()
        error = driver.find_element_by_id("errormsg_0_Passwd").text
        self.assertEqual(error, "Должно быть не более 200 символов")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

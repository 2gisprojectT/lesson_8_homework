import time
import unittest
from unittest import TestCase

from selenium import webdriver


class TestGmailAuth(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://mail.google.com/")
        self.driver.implicitly_wait(5)

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
        captcha = driver.find_element_by_id("identifier-captcha-input")
        startTime = time.time()
        while ((not captcha.is_displayed()) and ((time.time() - startTime) < 2)):
            email.send_keys("a")
            email.submit()
        self.assertTrue(captcha.is_displayed())

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

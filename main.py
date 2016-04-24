import unittest
from selenium import webdriver
from unittest import TestCase


def make_long_string(input_string, repeats):
    i = 0
    out_string = ""
    while i < repeats:
        out_string = out_string + input_string
        i += 1
    return out_string


class Test(TestCase):
    def setUp(self):
        """
        Начальные условия:
            1) Переходим на страницу mail.google.com
            2) Авторизируемся через логин и пароль
        """
        email = "2giskargapolovtest@gmail.com"
        passwd = "2GisKargapolovTestTest"
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get("http://mail.google.com/")
        self.driver.find_element_by_id("Email").send_keys(email)
        self.driver.find_element_by_id("next").click()
        self.driver.find_element_by_id("Passwd").send_keys(passwd)
        self.driver.find_element_by_id("signIn").click()

    def test_no_exist(self):
        """
        Шаги воспроизведения:
            1)Ввести в форму поиска текст, которого нет в письмах ящика.
            2)Нажать Enter.
        Ожидаемый результат:
            Вывод сообщения о том, что писем с таким текстом в ящике не найдено.
        """
        search_text = "some_text"
        self.driver.find_element_by_id("gbqfq").send_keys(search_text)
        self.driver.find_element_by_id('gbqfb').click()
        self.assertIn("Писем не найдено.", self.driver.page_source)

    def test_overflow(self):
        """
        Шаги воспроизведения:
            1)Ввести строку, превышающую максимальную допустимую длину.
            2)Нажать Enter.
        """
        search_text = make_long_string('overflow', 400)
        self.driver.find_element_by_id("gbqfq").send_keys(search_text)
        self.driver.find_element_by_id('gbqfb').click()
        self.assertIn("Слишком длинный поисковый запрос. Сократите его.", self.driver.page_source)

    def test_gramm_mistake(self):
        """
            Шаги воспроизведения:
                1)Ввести в форму поиска слово, с намеренной опечаткой (Н-р: молако).
                2)Нажать Enter.
            """
        search_text = "молако"
        self.driver.find_element_by_id("gbqfq").send_keys(search_text)
        self.driver.find_element_by_id('gbqfb').click()
        self.assertIn("Возможно, вы имели в виду:", self.driver.page_source)

    def test_size_mistake(self):
        """
        Шаги воспроизведения:
                1)нажать на кнопку "Показать параметры поиска"
                1)Ввести в форму под названием "Размер" строку, содержащую буквы.
                2)Нажать Enter.
        ОжидаемыЙ результат: Сообщение "Неверный запрос поиска – возврат всех писем"
        """
        search_text = "some_string"
        self.driver.find_element_by_id('gbqfab').click()
        self.driver.find_element_by_xpath("//input[@aria-label='Значение размера']").send_keys(search_text)
        self.driver.find_element_by_id('gbqfb').click()
        self.assertIn("Неверный запрос поиска", self.driver.page_source)

    def test_from(self):
        """
        Шаги воспроизведения:
                1)нажать на кнопку "Показать параметры поиска"
                1)Ввести в форму под названием "От" значение "Gmail".
                2)Нажать Enter.
        ОжидаемыЙ результат: Вывод списка сообщений от Gmail.
        """
        search_text = "Gmail"
        self.driver.find_element_by_id('gbqfab').click()
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/span/input").send_keys(search_text)
        self.driver.find_element_by_id('gbqfb').click()
        self.assertIn("Команда Gmail", self.driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main

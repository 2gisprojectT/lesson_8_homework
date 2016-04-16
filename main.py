from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
import unittest


class Test(TestCase):
    """
    Предусловия:
        1) Зайти на сайт dropbox.com/request и аутентифицироваться
    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.dropbox.com/requests")
        email = self.driver.find_element_by_xpath(".//input[@name='login_email']")
        passwd = self.driver.find_element_by_xpath(".//input[@name='login_password']")
        email.send_keys("evgenijkatunov@mail.ru")
        passwd.send_keys("test123")
        passwd.send_keys(Keys.RETURN)

    def test_empty_name(self):
        """
        Тест: Создание запроса файлов с пустой темой
        Действия:
            1) Нажать на кнопку создания запроса
            2) Оставить поле темы запроса пустым
            3) Перейти на следующий шаг мастера
        Проверить:
            Появление сообщения о необходимости ввести тему запроса
        """

        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_class_name("button-primary").click()
        error_msg = self.driver.find_element_by_class_name("text-input-error-wrapper")
        self.assertEqual("Введите тему вашего запроса файла.", error_msg.text)

    def test_more_then_maxlen_name(self):
        """
        Тест: Создание запроса файлов с темой больше максимальной длины
        Действия:
            1) Нажать на кнопку создания запроса
            2) Заполнить поле темы максимально допустимым числом символов
            3) Пройти остальные шаги мастера со значениями по умолчанию
        Проверить:
            Создан запрос с обрезанным наименованием до 140 символов
        """

        name = "a" * 141;
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(name)
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_element_by_class_name("dbmodal-button").click()
        self.driver.refresh()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.assertEqual(name[:140], self.driver.find_element_by_name("drops_title").get_attribute("value"))

    def test_unresolved_symbol_name(self):
        """
        Тест:
            Создание запроса файлов с недопустимым символом в теме
        Действия:
            1) Нажать на кнопку создания запроса
            2) Ввести в поле темы строку с недопустимыми символами
        Проверить:
            Появление сообщения о вводе недопустимых символов
        """

        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys("test/test")
        error_msg = self.driver.find_element_by_class_name("text-input-error-wrapper")
        self.assertEqual("В названиях запрещено использовать косую черточку (/). Пожалуйста, выберите другое название.",
                         error_msg.text)

    def test_overdue_downloads_never(self):
        """
        Тест:
            Создание запроса файлов с указанием срока просроченной загрузки "Никогда"
        Действия:
            1) Начать создавать запрос с корректной темой
            2) Выставить checkBox "Срок"
            3) Выбрать в поле просроченные загрузки: Никогда
            4) Пройти остальные шаги мастера со значениями по умолчанию
        Проверить:
            Создан запрос без периода просроченной загрузки
        """

        name = "TEST2"
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(name)
        self.driver.find_element_by_id("enable-deadlines-checkbox").click()
        # клик по "+Разрешить просроченные загрузки"
        self.driver.find_element_by_xpath(".//a[@data-reactid='.3.1.0.0.2.0.2.$deadline-description.0.1']").click()
        # клик по выпадающему списку со сроками просроченной загрузки
        self.driver.find_element_by_xpath(".//div[@data-reactid='.3.1.0.0.2.0.2.$deadline-description2.1.2']").click()
        self.driver.find_element_by_xpath(".//div[@title='Никогда']").click()
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_element_by_class_name("dbmodal-button").click()
        self.driver.refresh()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.assertEqual(name, self.driver.find_element_by_name("drops_title").get_attribute("value"))
        self.assertEqual(True,
                         self.driver.find_element_by_xpath(
                             ".//a[@data-reactid='.3.1.0.0.2.0.2.$deadline-description.0.1']").is_displayed())

    def test_overdue_downloads_notnever(self):
        """
        Тест:
            Создание запроса файлов с указанием срока просроченной загрузки отличным от "Никогда"
        Действия:
            1) Начать создавать запрос с корректным наименованием
            2) Выставить checkBox "Срок"
            3) Выбрать в поле просроченные загрузки: в течение одного дня
            4) Пройти остальные шаги мастера со значениями по умолчанию
        Проверить:
            Создан запрос с заданным сроком загрузки
        """

        name = "TEST3"
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(name)
        self.driver.find_element_by_id("enable-deadlines-checkbox").click()
        # клик по "+Разрешить просроченные загрузки"
        self.driver.find_element_by_xpath(".//a[@data-reactid='.3.1.0.0.2.0.2.$deadline-description.0.1']").click()
        # клик по выпадающему списку со сроками просроченной загрузки
        self.driver.find_element_by_xpath(".//div[@data-reactid='.3.1.0.0.2.0.2.$deadline-description2.1.2']").click()
        self.driver.find_element_by_xpath(".//div[@title='В течении одного дня']").click()
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_element_by_class_name("dbmodal-button").click()
        self.driver.refresh()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.assertEqual(name, self.driver.find_element_by_name("drops_title").get_attribute("value"))
        self.assertEqual("В течении одного дня",
                         self.driver.find_element_by_xpath(
                             ".//div[@data-reactid='.3.1.0.0.2.0.2.$deadline-description2.1.2.0']")
                         .get_attribute("Title"))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main();

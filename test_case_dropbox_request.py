import unittest
from unittest import TestCase
from selenium import webdriver
from datetime import datetime, timedelta
from ddt import ddt, data
import locale


@ddt
class DropboxTest(TestCase):
    def setUp(self):
        """ Предусловие: зайти на сайт dropbox.com, аутентифицироваться """
        locale.setlocale(locale.LC_ALL, "russian")
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.dropbox.com")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("sign-in").click()
        self.driver.find_element_by_xpath(".//input[@name='login_email']").send_keys("testcase.dropbox@mail.ru")
        self.driver.find_element_by_xpath(".//input[@name='login_password']").send_keys("projectT111")
        self.driver.find_element_by_class_name("login-button").click()

    @data(["Т", None],
          ["Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс", "Запросы файлов"])
    def test_create_request_pairwise_without_time_download(self, value):
        """
        Заголовок: Запрос без срока загрузки
        Шаги
            1. Нажать на кнопку "Запросить файлы".
            2. В поле "Какой файл вам нужен?" ввести значение колонки "Наименование/описание файла".
            3. В поле "В какой папке в вашем Dropbox следует разместить файлы?" выполнить действие, указанное в колонке "Папка, куда поместить файл".
            4. Опцию "Добавить срок" оставить выключенной.
            5. Нажать кнопку "Далее".
            6. В появившемся окне "Отправить запрос файла" нажать кнопку "Копировать ссылку" и нажать кнопку "Готово"
            7. В соседней вкладке браузера перейти по ссылке, скопированной в п.3.6.
        Проверки:
            1. На странице запросов файлов (https://www.dropbox.com/requests) появился созданный запрос.
            2. На странице п.3.7 отображен функционал загрузки созданного запроса.
        """
        self.driver.find_element_by_class_name("drops-nav-item").click()
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(value[0])
        if value[1] is not None:
            self.driver.find_element_by_class_name("create-edit-form-destination-change").click()
            self.driver.find_element_by_xpath(".//span[@data-reactid='.3.1.0.0.2.0.1.0.0.0.1.0.$/"+value[1]+".0']").click()
            self.driver.find_element_by_class_name("choose-folder-buttons").click()
        self.driver.find_element_by_class_name("button-primary").click()
        link = self.driver.find_element_by_id("drop-link-field").get_attribute("value")
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.driver.find_element_by_class_name("create-edit-form").click()
        request_name = self.driver.find_element_by_class_name("text-input-input").get_attribute("value")
        self.assertEqual(value[0], request_name)
        self.driver.get(link)
        info = self.driver.find_element_by_class_name("info__title")
        self.assertEqual(value[0], info.text)

    @data(["Т", None],
          ["Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс", "Запросы файлов"])
    def test_create_request_pairwise_time_download_present_day(self, value):
        """
        Заголовок: Запрос со сроком загрузки "текущая дата"
        Предусловие: Тест выполнить раньше 23:00
        Шаги
            1. Нажать на кнопку "Запросить файлы".
            2. В поле "Какой файл вам нужен?" ввести значение колонки "Наименование/описание файла".
            3. В поле "В какой папке в вашем Dropbox следует разместить файлы?" выполнить действие, указанное в колонке "Папка, куда поместить файл".
            4. Опцию "Добавить срок" включить.
            5. В поле с датой указать текущую дату.
            6. В поле с временем указать время, превышающее текущее время (23:00).
            7. Нажать кнопку "Далее".
            8. В появившемся окне "Отправить запрос файла" нажать кнопку "Копировать ссылку" и нажать кнопку "Готово"
            9. В соседней вкладке браузера перейти по ссылке, скопированной в п.3.6.
        Проверки:
            1. На странице запросов файлов (https://www.dropbox.com/requests) появился созданный запрос.
            2. На странице п.3.7 отображен функционал загрузки созданного запроса с указанным сроком загрузки(п.3.5-3.6).
        """
        self.driver.find_element_by_class_name("drops-nav-item").click()
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(value[0])
        if value[1] is not None:
            self.driver.find_element_by_class_name("create-edit-form-destination-change").click()
            self.driver.find_element_by_xpath(".//span[@data-reactid='.3.1.0.0.2.0.1.0.0.0.1.0.$/"+value[1]+".0']").click()
            self.driver.find_element_by_class_name("choose-folder-buttons").click()
        self.driver.find_element_by_id("enable-deadlines-checkbox").click()
        self.driver.find_element_by_class_name("c-input").click()
        download_day = datetime.today()
        self.driver.find_element_by_id("day" + str(download_day.day) + "-" + str(download_day.month - 1)).click()
        self.driver.find_element_by_class_name("c-time-selector").click()
        self.driver.find_element_by_xpath(".//div[@title='23:00 ']").click()
        self.driver.find_element_by_class_name("button-primary").click()
        link = self.driver.find_element_by_id("drop-link-field").get_attribute("value")
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.driver.find_element_by_class_name("create-edit-form").click()
        request_name = self.driver.find_element_by_class_name("text-input-input").get_attribute("value")
        self.assertEqual(value[0], request_name)
        self.driver.get(link)
        info = self.driver.find_element_by_class_name("info__title")
        self.assertEqual(value[0], info.text)
        text_deadline = self.driver.find_element_by_class_name("file_collector__deadlines-pill").text
        time_download = download_day.strftime('%B').lower() + " " + str(download_day.day) + ", " \
                        + str(download_day.year) + " 23:00"
        self.assertIn(time_download, text_deadline)

    @data(["Т", None, 1, "Никогда"],
          ["Т", "Запросы файлов", 3, "В течении одного дня"],
          ["Т", None, 7, "В течение двух дней"],
          ["Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс", "Запросы файлов", 1, "В течение недели"],
          ["Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс", None, 3, "В течение 30 дней"],
          ["Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс", "Запросы файлов", 7, "Всегда"])
    def test_create_request_pairwise_overdue_download(self, value):
        """
        Заголовок: Запрос со сроком загрузки больше текущей даты и включенной опцией просроченных загрузок
        Шаги
            1. Нажать на кнопку "Запросить файлы".
            2. В поле "Какой файл вам нужен?" ввести значение колонки "Наименование/описание файла".
            3. В поле "В какой папке в вашем Dropbox следует разместить файлы?" выбрать указанную папку или не задавать папку (None).
            4. Опцию "Добавить срок" включить.
            5. В поле с датой указать дату срока загрузки.
            6. В поле с временем валидное время(11:00).
            7. Нажать на выделенный текст "+ Разрешить просроченные загрузки", в выпадающем списке "Разрешить просроченные загрузки:" указать значение из колонки "Опция просроченных загрузок"
            8. Нажать кнопку "Далее".
            9. В появившемся окне "Отправить запрос файла" нажать кнопку "Копировать ссылку" и нажать кнопку "Готово"
            10. В соседней вкладке браузера перейти по ссылке, скопированной в п.3.6.
        Проверки:
            1. На странице запросов файлов (https://www.dropbox.com/requests) появился созданный запрос.
            2. На странице п.3.7 отображен функционал загрузки созданного запроса с указанным сроком загрузки(п.3.5-3.6).
        """
        self.driver.find_element_by_class_name("drops-nav-item").click()
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(value[0])
        if value[1] is not None:
            self.driver.find_element_by_class_name("create-edit-form-destination-change").click()
            self.driver.find_element_by_xpath(".//span[@data-reactid='.3.1.0.0.2.0.1.0.0.0.1.0.$/"+value[1]+".0']").click()
            self.driver.find_element_by_class_name("choose-folder-buttons").click()
        self.driver.find_element_by_id("enable-deadlines-checkbox").click()
        self.driver.find_element_by_class_name("c-input").click()
        download_day = datetime.today() + timedelta(days=value[2])
        self.driver.find_element_by_id("day" + str(download_day.day) + "-" + str(download_day.month - 1)).click()
        self.driver.find_element_by_class_name("c-time-selector").click()
        self.driver.find_element_by_xpath(".//div[@title='11:00 ']").click()
        self.driver.find_element_by_xpath(".//a[@data-reactid='.3.1.0.0.2.0.2.$deadline-description.0.1']").click()
        self.driver.find_element_by_class_name("c-deadlines__grace-period-selector").click()
        self.driver.find_element_by_xpath(".//div[@title='"+value[3]+"']").click()
        self.driver.find_element_by_class_name("button-primary").click()
        link = self.driver.find_element_by_id("drop-link-field").get_attribute("value")
        self.driver.find_element_by_class_name("button-primary").click()
        self.driver.find_elements_by_class_name("actions__link")[0].click()
        self.driver.find_element_by_class_name("create-edit-form").click()
        request_name = self.driver.find_element_by_class_name("text-input-input").get_attribute("value")
        self.assertEqual(value[0], request_name)
        self.driver.get(link)
        info = self.driver.find_element_by_class_name("info__title")
        self.assertEqual(value[0], info.text)
        text_deadline = self.driver.find_element_by_class_name("file_collector__deadlines-pill").text
        time_download = download_day.strftime('%B').lower() + " " + str(download_day.day) + ", " \
                        + str(download_day.year) + " 11:00"
        self.assertIn(time_download, text_deadline)

    @data(["Тест \ : ? * \" |", "Не допускаются угловые скобки, а также следующие символы: \ / : ? * \" |"],
          ["   ", "Введите тему вашего запроса файла."])
    def test_negative_create_request_invalid_name_notify(self, value):
        """
        Заголовок: Невалидное наименование запроса
        Шаги
            1. Нажать на кнопку "Запросить файлы".
            2. В поле "Какой файл вам нужен?" ввести значение колонки "Наименование/описание файла".
            3. В поле "В какой папке в вашем Dropbox следует разместить файлы?" не задавать папку.
            4. Опцию "Добавить срок" оставить выключенной.
            5. Нажать кнопку "Далее".
        Проверки:
            1. Всплывает предупреждение пользователя.
        """
        self.driver.find_element_by_class_name("drops-nav-item").click()
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys(value[0])
        self.driver.find_element_by_class_name("button-primary").click()
        notify = self.driver.find_element_by_id("notify-msg").text
        self.assertEqual(value[1], notify)

    def test_negative_create_request_invalid_name_max_length(self):
        """
        Заголовок: Длина наименования запроса max+1
        Шаги
            1. Нажать на кнопку "Запросить файлы".
            2. В поле "Какой файл вам нужен?" ввести "Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французсК".
        Проверки:
            1. Последний символ из наименования файла не удается ввести.
        """
        self.driver.find_element_by_class_name("drops-nav-item").click()
        self.driver.find_element_by_class_name("drops-grid-create-new-item").click()
        self.driver.find_element_by_name("drops_title").send_keys("Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французсК")
        request_name = self.driver.find_element_by_class_name("text-input-input").get_attribute("value")
        self.assertEqual(request_name, "Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французских булок, да выпей чаю. Съешь ещё этих мягких французс")

    def tearDown(self):
        """ Завершение сессии """
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
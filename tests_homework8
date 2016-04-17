import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select


class TestCases(TestCase):
    def setUp(self):
        """
        Инициализация драйвера для тестирования:
            [1] Инициализируем тестовые данные.
            [2] Открываем сайт.
            [3] Переходим в личный кабинет.
        """
        self.email = "antonprojectt@leeching.net"
        self.password = "test009"
        self.new_password = "qwerty"
        self.passenger_info = ("IVANOV", "IVAN", "12.12.1990", "123QWE", "12.12.2100")
        self.country = {"Венгрия": "HU"}

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get("https://www.onetwotrip.com/ru/")
        self.driver.find_element_by_class_name("enter").click()

    def test_incorrect_authorization(self):
        """
        Шаги воспроизведения:
            [1] В поле "Электронная почта" ввести почту зарегистрированную на onetwotrip.com.
            [2] В поле "Пароль" ввести произвольные буквы и цифры.
            [3] Кликнуть по кнопке "Войти".
        Ожидаемый результат:
            [*] Авторизация не проходит, ниже поля "пароль" появляется красное окошко, уведомляющая об ошибке.
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys(self.email)
        driver.find_element_by_id("input_auth_pas").send_keys("123456")
        driver.find_element_by_class_name("pos_but").click()
        error_info = driver.find_element_by_class_name("Error").text
        self.assertTrue(driver.find_element_by_class_name("Error").is_displayed())
        self.assertEqual(error_info, "Неправильный пароль или почта")

    def test_twitter_authorization(self):
        """
        Шаги воспроизведения:
            [1] Нажать на лого Twitter.
            [2] В открывшимся окне ввести данные от аккаунта Twitter.
            [3] Нажать кнопку "Войти".
        Ожидаемый результат:
            [*] Настройках профиля пользователя, в пункте "Авторизация" появится надпись "Twitter".
        """
        driver = self.driver
        driver.find_element_by_css_selector(".sLinks_inside > ul:nth-child(2) > li:nth-child(2)").click()

        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_id("username_or_email").send_keys(self.email)
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_id("allow").submit()
        driver.switch_to.window(driver.window_handles[0])

        driver.find_element_by_class_name("knownUser").click()
        user = driver.find_element_by_class_name("reg").text
        self.assertEqual(user, "АВТОРИЗАЦИЯ\nTwitter")

    def test_add_passenger_to_address_book(self):
        """
        Шаги воспроизведения:
            [1] Авторизироваться и перейти в свой профиль.
            [2] Кликнуть по кнопке "Добавить пассажира".
            [3] В поля ввести валидные значения.
            [4] Кликнуть по кнопке "Сохранить изменения".
            [5] Обновить страницу браузера.
        Ожидаемый результат:
            [*] Добавится новый пассажир, информация о пассажире соответствует ранее введеной.
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys(self.email)
        driver.find_element_by_id("input_auth_pas").send_keys(self.password)
        driver.find_element_by_class_name("pos_but").click()
        driver.find_element_by_class_name("knownUser").click()
        driver.find_element_by_id("button_addPassenger").click()

        driver.find_element_by_id("input_lastName0").send_keys(self.passenger_info[0])
        driver.find_element_by_id("input_firstName0").send_keys(self.passenger_info[1])
        driver.find_element_by_id("input_birthDate0").send_keys(self.passenger_info[2])
        driver.find_element_by_id("input_passNumber0").send_keys(self.passenger_info[3])
        driver.find_element_by_id("input_passExpDate0").send_keys(self.passenger_info[4])
        driver.find_element_by_id("button_savePassengers").click()

        driver.refresh()

        last_name_field = driver.find_element_by_id("input_lastName0").get_attribute("value")
        first_name_field = driver.find_element_by_id("input_firstName0").get_attribute("value")
        birth_date_field = driver.find_element_by_id("input_birthDate0").get_attribute("value")
        pass_number_field = driver.find_element_by_id("input_passNumber0").get_attribute("value")
        pass_exp_date_field = driver.find_element_by_id("input_passExpDate0").get_attribute("value")

        self.assertEqual(last_name_field, self.passenger_info[0])
        self.assertEqual(first_name_field, self.passenger_info[1])
        self.assertEqual(birth_date_field, "12 дек 1990")
        self.assertEqual(pass_number_field, self.passenger_info[3])
        self.assertEqual(pass_exp_date_field, self.passenger_info[4])

    def test_select_country(self):
        """
        Шаги воспроизведения:
            [1] Авторизироваться и перейти в свой профиль.
            [2] Выбрать страну в поле "Страна".
            [3] Кликнуть по кнопке "Сохранить изменения".
            [4] Обновить страницу.
        Ожидаемый результат:
            [*] В поле "Страна" отобразиться ранее выбранное значение.
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys(self.email)
        driver.find_element_by_id("input_auth_pas").send_keys(self.password)
        driver.find_element_by_class_name("pos_but").click()
        driver.find_element_by_class_name("knownUser").click()

        country_field = driver.find_element_by_name("country")
        select = Select(country_field)
        select.select_by_value(self.country.get("Венгрия"))
        driver.find_element_by_id("button_saveContacts").submit()

        driver.refresh()

        country_field = driver.find_element_by_name("country").get_attribute("value")
        self.assertEqual(country_field, self.country.get("Венгрия"))

    def test_change_password(self):
        """
        Шаги воспроизведения:
            [1] Авторизироваться и перейти в свой профиль.
            [2] Нажать "Сменить пароль".
            [3] В поле "Новый пароль" ввести новый пароль.
            [4] В поле "Повторите новый пароль" повторить ввод нового пароля.
            [5] Кликнуть по кнопке "Сохранить изменения".
        Ожидаемый результат:
            [*] Появится окошко с информацией о смене пароля.
        """
        driver = self.driver
        driver.find_element_by_id("input_auth_email").send_keys(self.email)
        driver.find_element_by_id("input_auth_pas").send_keys(self.password)
        driver.find_element_by_class_name("pos_but").click()
        driver.find_element_by_class_name("knownUser").click()
        driver.find_element_by_class_name("change_pas").click()

        new_password_field = driver.find_element_by_id("input_newPas")
        repeat_new_password_field = driver.find_element_by_id("input_repeatPas")

        new_password_field.send_keys(self.new_password)
        repeat_new_password_field.send_keys(self.new_password)

        driver.find_element_by_id("button_changePassword").submit()
        info = driver.find_element_by_class_name("reason").text
        self.assertTrue(driver.find_element_by_class_name("reason").is_displayed())
        self.assertEqual(info, "Изменение пароля")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

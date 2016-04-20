from selenium import webdriver
from unittest import TestCase
import unittest

class Test(TestCase):
    """
    Предусловия:
        1) Зайти на сайт dropbox.com/login?src=logout/
        2) Перейти в создание аккаунта
    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1200,768)
        self.driver.get("https://www.dropbox.com/login?src=logout/")
        self.driver.implicitly_wait(15)
        self.driver.find_element_by_class_name("login-register-switch-link").click()

        self.correct_name_value = "test_name"
        self.correct_email_value = "test_email@test.ru"
        self.password_value = "password123"

    def test_register_with_google(self):
        """
        Тест: Проверка регистрации через Google
        Шаги:
            1. Нажать кнопку "Зарегистрироваться через Google"
            2. В открывшемся окне авторизации в поле для электронной почты ввести верный адрес электронной почты
            3. Нажать кнопку "Далее"
            4. В открывшейся вкладке в поле ввода пароля ввести верный пароль
            5. Нажать кнопку "Войти"
        Ожидаемый результат:
            1. В открывшемся окне произошла авторизация в введенный аккаунт
        """
        driver = self.driver
        correct_google_login = "projectt_google"
        google_password_value = "password_google"
        button_register_with_google = driver.find_element_by_class_name("auth-google")
        button_register_with_google.click()
        window_after = self.driver.window_handles[1]
        driver.switch_to.window(window_after)
        google_mail = driver.find_element_by_name("Email")
        google_mail.send_keys(correct_google_login)
        google_mail.submit()
        google_password = driver.find_element_by_name("Passwd")
        google_password.send_keys(google_password_value)
        google_password.submit()
        page_header = self.driver.find_element_by_class_name("gb_b")
        page_header.click()
        google_account_name = driver.find_element_by_class_name("gb_pb")
        self.assertEqual(str(correct_google_login) + "@gmail.com", google_account_name.text)

    def test_captcha_information(self):
        """
        Тест: Проверка выдачи информации о капче
        Шаги:
            1. В обязательные для заполнения поля ввести корректные значения
            2. Отметить галочку «Я принимаю Условия обслуживания Dropbox»
            3. Нажать кнопку "Зарегистрироваться"
            4. В появившейся форме с капчей нажать кнопку с вопросительным знаком
        Ожидаемый результат:
            1. Открылась новая вкладка с информацией о капче
        """
        driver = self.driver
        input_data = driver.find_elements_by_class_name("text-input-input")
        register_name = input_data[4]
        register_email = input_data[6]
        register_name.send_keys(self.correct_name_value)
        register_email.send_keys(self.correct_email_value)
        input_password = driver.find_elements_by_class_name("password-input")
        input_password[1].send_keys(self.password_value)
        agree_checkbox = self.driver.find_elements_by_name("tos_agree")
        agree_checkbox[1].click()
        sign_up_button =  self.driver.find_elements_by_class_name("login-button")
        sign_up_button[2].click()
        captcha_info = driver.find_elements_by_class_name("recaptcha-button")
        captcha_info[3].click()
        window_after = self.driver.window_handles[1]
        driver.switch_to.window(window_after)
        self.assertEqual("reCAPTCHA Help", driver.title)

    def test_go_to_sign_in(self):
        """
        Тест: Проверка перенаправления на окно входа в уже существующий аккаунт
        Шаги:
            1. Ввести в поле «e-mail» уже зарегистрированный адрес электронной почты
            2. В остальные обязательные для заполнения поля ввести корректные значения
            3. Отметить галочку «Я принимаю Условия обслуживания Dropbox»
            4. Нажать кнопку зарегистрироваться
            5. Перейти по появившейся ссылке "Ввойдите в систему"
        Ожидаемый результат:
            1. Откроется окно для входа в существующий аккаунт
        """
        driver = self.driver
        existing_email_value = "user@mail.ru"
        input_data = driver.find_elements_by_class_name("text-input-input")
        register_name = input_data[4]
        register_email = input_data[6]
        register_name.send_keys(self.correct_name_value)
        register_email.send_keys(existing_email_value)
        input_password = driver.find_elements_by_class_name("password-input")
        input_password[1].send_keys(self.password_value)
        agree_checkbox = driver.find_elements_by_name("tos_agree")
        agree_checkbox[1].click()
        sign_up_button =  driver.find_elements_by_class_name("login-button")
        sign_up_button[2].click()
        sign_in_link = driver.find_elements_by_class_name("login-register-switch-link")
        sign_in_link[1].click()
        register_header = driver.find_element_by_class_name("login-register-header")
        self.assertEqual("Войти", register_header.text)


    def test_hint_easy_password(self):
        """
        Тест: Проверка подсказки к вводу слабого пароля
        Шаги:
            1. В обязательные для заполнения поля ввести корректные значения
            2. В поле «Пароль» ввести строку длиной 10 символов, состоящую из цифр
            3. Нажать на иконку сложности пароля
        Ожидаемый результат:
            1. Во всплывающем окне подсказки написано "Слабый"
        """
        driver = self.driver
        easy_password = 10 * '5'
        input_data = driver.find_elements_by_class_name("text-input-input")
        register_name = input_data[4]
        register_email = input_data[6]
        register_name.send_keys(self.correct_name_value)
        register_email.send_keys(self.correct_email_value)
        input_password = driver.find_elements_by_class_name("password-input")
        input_password[1].send_keys(easy_password)
        protection_meter = driver.find_element_by_class_name("password-input-meter")
        protection_meter.click()
        hint_message = driver.find_element_by_class_name("password-bubble-title")
        self.assertEqual("Слабый", hint_message.text)

    def test_maximum_length_name(self):
        """
        Тест: Проверка ввода в поле Имя значения больше максимального граничного
        Шаги:
            1. Ввести в поле «Имя» строку длиной больше 100 символов
            2. Поле «Фамилия» оставить пустым
            3. В остальные обязательные для заполнения поля ввести корректные значения
            4. Нажать кнопку зарегистрироваться
        Ожидаемый результат:
            1. Над полем «Имя» высветится ошибка «Введите значение: менее 100 символов»
        """
        driver = self.driver
        maximum_name_value = 'a' * 105
        input_data = driver.find_elements_by_class_name("text-input-input")
        register_name = input_data[4]
        register_email = input_data[6]
        register_name.send_keys(maximum_name_value)
        register_email.send_keys(self.correct_email_value)
        input_password = driver.find_elements_by_class_name("password-input")
        input_password[1].send_keys(self.password_value)
        agree_checkbox = driver.find_elements_by_name("tos_agree")
        agree_checkbox[1].click()
        sign_up_button =  self.driver.find_elements_by_class_name("login-button")
        sign_up_button[2].click()
        error_message = self.driver.find_element_by_class_name("error-message")
        self.assertEqual("Введите значение: менее 100 символов.", error_message.text)

    def tearDown(self):
       self.driver.quit()

if __name__ == '__main__':
    unittest.main()
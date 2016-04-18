from selenium import webdriver
import unittest

class auto_test_gmail(unittest.TestCase):

    def setUp(self):
        """
           Предусловие:
           Зайти на страницу регистрации mail.google.com
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default")
        self.driver.implicitly_wait(10)

    def test_email_only_numbers(self):
        """
           Тест кейс "Проверка вывода ошибки при вводе в поле email больще 8 цифр"
           Шаги:
            1.Заполнить поля "Имя" и "Фамилия" валидными значениями.
            2.Ввести в поле "Имя пользователя" строку из 9-ти символов, полностью состоящую из цифр.
            3.Нажать кнопку "Далее".
           Ожидание:
            Внизу поля "Имя пользователя" появляется надпись "Имя пользователя, состоящее из 8 или более символов, должно включать хотя бы одну латинскую букву (a-z)"
        """
        name = self.driver.find_element_by_id("FirstName")
        name.send_keys("Петя")
        last_name = self.driver.find_element_by_id("LastName")
        last_name.send_keys("Иванов")
        email = self.driver.find_element_by_id("GmailAddress")
        email.send_keys("123456789")
        button = self.driver.find_element_by_id("submitbutton").click()
        error_msg = self.driver.find_element_by_id("errormsg_0_GmailAddress").text
        self.assertTrue(self.driver.find_element_by_id("errormsg_0_GmailAddress").is_displayed())
        self.assertEqual(error_msg, "Имя пользователя, состоящее из 8 или более символов, должно включать хотя бы одну латинскую букву (a-z)")

    def test_min_email(self):
        """
           Тест кейс "Проверка вывода ошибки при вводе в поле email строки, меньше минимально возможной"
           Шаги:
            1.Заполнить поля "Имя" и "Фамилия" валидными значениями.
            2.Ввод любых 5-ти символов в поле "Имя пользователя".
            3.Нажать кнопку "Далее".
           Ожидание:
            Внизу поля "Имя пользователя" появляется надпись "Допустимое количество символов: 6–30"
        """
        name = self.driver.find_element_by_id("FirstName")
        name.send_keys("Петя")
        last_name = self.driver.find_element_by_id("LastName")
        last_name.send_keys("Иванов")
        email = self.driver.find_element_by_id("GmailAddress")
        email.send_keys("qwert")
        button = self.driver.find_element_by_id("submitbutton").click()
        error_msg = self.driver.find_element_by_id("errormsg_0_GmailAddress").text
        self.assertTrue(self.driver.find_element_by_id("errormsg_0_GmailAddress").is_displayed())
        self.assertEqual(error_msg, "Допустимое количество символов: 6–30.")

    def test_max_length_passwd(self):
        """
           Тест кейс "Проверка вывода ошибки при вводе в поле "Пароль" строки, больше максимально возможной"
            Шаги:
             1.Заполнить поля "Имя" и "Фамилия", "Имя пользователя" валидными значениями.
             2.Ввести в поле "Пароль" строку, состоящую из 101 символа
             3.Нажать кнопку "Далее".
            Ожидание:
            Внизу поля "Пароль" появляется надпись "Должно быть не более 100 символов"

        """
        name = self.driver.find_element_by_id("FirstName")
        name.send_keys("Петя")
        last_name = self.driver.find_element_by_id("LastName")
        last_name.send_keys("Иванов")
        email = self.driver.find_element_by_id("GmailAddress")
        email.send_keys("petyaivanov0981")
        passwd = self.driver.find_element_by_id("Passwd")
        s = "a"
        for i in range (0, 100):
            s += "a"
        passwd.send_keys(s)
        button = self.driver.find_element_by_id("submitbutton").click()
        error_msg = self.driver.find_element_by_id("errormsg_0_Passwd").text
        self.assertTrue(self.driver.find_element_by_id("errormsg_0_Passwd").is_displayed())
        self.assertEqual(error_msg, "Должно быть не более 100 символов")

    def test_passwd_frequent(self):
        """
           Тест кейс "Проверка вывода ошибки при вводе в поле "Пароль" часто встречающейся комбинации символов"
            Шаги:
             1.Заполнить поля "Имя" и "Фамилия", "Имя пользователя" валидными значениями.
             2.Ввести в поле "Пароль" строку, состоящую из распространенной комбинации символов
             3.Нажать кнопку "Далее".
            Ожидание:
            Внизу поля "Пароль" появляется надпись "Этот пароль очень распространен. Защитите аккаунт от взлома – придумайте более сложный пароль."
        """
        name = self.driver.find_element_by_id("FirstName")
        name.send_keys("Петя")
        last_name = self.driver.find_element_by_id("LastName")
        last_name.send_keys("Иванов")
        email = self.driver.find_element_by_id("GmailAddress")
        email.send_keys("petyaivanov0981")
        passwd = self.driver.find_element_by_id("Passwd")
        passwd.send_keys("12345qwerty")
        button = self.driver.find_element_by_id("submitbutton").click()
        error_msg = self.driver.find_element_by_id("errormsg_0_Passwd").text
        self.assertTrue(self.driver.find_element_by_id("errormsg_0_Passwd").is_displayed())
        self.assertEqual(error_msg, "Этот пароль очень распространен. Защитите аккаунт от взлома – придумайте более сложный пароль.")

    def test_captcha(self):
        """
           Тест кейс "Проверка исчезновения картинки с капчей при отметке чекбокса "Пропустить проверку на робота" "
            Шаги:
             1. Убедиться что на форме есть картинка с капчей
             2. Отметить чекбокс "Пропустить проверку на робота. Может потребоваться проверка по телефону."
            Ожидание:
             Исчезает картинка с капчей, проверка на робота на данном этапе считается успешной.
        """
        captcha = self.driver.find_element_by_id("recaptcha_challenge_image")
        self.assertTrue(self.driver.find_element_by_id("recaptcha_challenge_image").is_displayed())
        check = self.driver.find_element_by_id("SkipCaptcha").click()
        self.assertFalse(self.driver.find_element_by_id("recaptcha_challenge_image").is_displayed())

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main();
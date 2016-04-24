from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest


class GmailSendingTests(unittest.TestCase):
    def setUp(self):
        """
        Предусловия:
        1) Зайти на mail.google.com
        2) Авторизоваться
        3) Нажать на кнопку "Написать"
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://mail.google.com")
        email = self.driver.find_element_by_name("Email")
        email.send_keys("arch.step.inc@gmail.com", Keys.RETURN)
        passw = WW(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Passwd")))
        passw.send_keys("TestinG1234", Keys.RETURN)
        WW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "z0"))).click()

    def testAllFilledFields(self):
        """
        Шаги:
        1) Заполнить поле "Получатели" в формате: ____@____.____
        2) Заполнить оставшиеся поля
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Форма отправки закроется, через некоторое время в центре экрана появится сообщение об успешной доставке
        """
        WW(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "to"))).send_keys("arch.step.inc@gmail.com ")
        self.driver.find_element_by_name("subjectbox").send_keys("Hello")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "vh"),"Письмо отправлено. Просмотреть сообщение"))
        self.assertTrue(mes)

    def testNoTheme(self):
        """
        Шаги:
        1) Заполнить поле "Получатели" в формате: ____@____.____
        2) Поле "Тема" оставить пустым
        3) Заполнить поле "Тело письма"
        4) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Форма отправки закроется, через некоторое время в центре экрана появится сообщение об успешной доставке
        """
        WW(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "to"))).send_keys("arch.step.inc@gmail.com ")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "vh"),"Письмо отправлено. Просмотреть сообщение"))
        self.assertTrue(mes)

    def testWrongDestination(self):
        """
        Шаги:
        1) Поле "Получатели" заполнить текстом, не являющегося адресом
        2) Заполнить поле "Тело письма"
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Появится сообщение об ошибке
        """
        WW(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "to"))).send_keys("курлык")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "Kj-JD-Jz"), "Адрес курлык в поле Кому не распознан. Проверьте правильность ввода всех адресов."))
        self.assertTrue(mes)

    def testNoReceivers(self):
        """
        Шаги:
        1) Поле "Получатели" не заполнять
        2) Заполнить поле "Тело письма"
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Появится сообщение об ошибке
        """
        WW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "LW-avf"))).send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "Kj-JD-Jz"), "Укажите как минимум одного получателя."))
        self.assertTrue(mes)

    def testDynamicSave(self):
        """
        Шаги:
        1) Заполнить любое поле (можно одним символом)
        2) Подождать пару секунд

        Ожидаемый результат:
        В нижней части формы отправки справа появится надпись: "Идет сохранение", а затем: "Сохранено".
        """
        WW(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "to"))).send_keys("a")
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "aWQ"), "Идет сохранение"))
        self.assertTrue(mes)
        mes = WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "aWQ"), "Сохранено"))
        self.assertTrue(mes)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

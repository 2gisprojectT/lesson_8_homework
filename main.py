from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC
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
        self.driver.implicitly_wait(20)
        self.driver.get("https://mail.google.com")
        self.driver.find_element_by_name("Email").send_keys("arch.step.inc@gmail.com", Keys.RETURN)
        self.driver.find_element_by_id("Passwd").send_keys("TestinG1234", Keys.RETURN)
        self.driver.find_element_by_class_name("z0").click()

    def test_all_filled_fields(self):
        """
        Шаги:
        1) Заполнить поле "Получатели" в формате: ____@____.____
        2) Заполнить оставшиеся поля
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Форма отправки закроется, через некоторое время в центре экрана появится сообщение об успешной доставке
        """
        self.driver.find_element_by_name("to").send_keys("arch.step.inc@gmail.com ")
        self.driver.find_element_by_name("subjectbox").send_keys("Hello")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = self.wait_text("vh", "Письмо отправлено. Просмотреть сообщение")
        self.assertTrue(mes)

    def test_no_theme(self):
        """
        Шаги:
        1) Заполнить поле "Получатели" в формате: ____@____.____
        2) Поле "Тема" оставить пустым
        3) Заполнить поле "Тело письма"
        4) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Форма отправки закроется, через некоторое время в центре экрана появится сообщение об успешной доставке
        """
        self.driver.find_element_by_name("to").send_keys("arch.step.inc@gmail.com ")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = self.wait_text("vh", "Письмо отправлено. Просмотреть сообщение")
        self.assertTrue(mes)

    def test_wrong_destination(self):
        """
        Шаги:
        1) Поле "Получатели" заполнить текстом, не являющегося адресом
        2) Заполнить поле "Тело письма"
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Появится сообщение об ошибке
        """
        self.driver.find_element_by_name("to").send_keys("курлык")
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = self.wait_text("Kj-JD-Jz", "Адрес курлык в поле Кому не распознан. Проверьте правильность ввода всех адресов.")
        self.assertTrue(mes)

    def test_no_receivers(self):
        """
        Шаги:
        1) Поле "Получатели" не заполнять
        2) Заполнить поле "Тело письма"
        3) Нажать на кнопку "Отправить"

        Ожидаемый результат:
        Появится сообщение об ошибке
        """
        self.driver.find_element_by_class_name("LW-avf").send_keys("Hello", Keys.TAB, Keys.ENTER)
        mes = self.wait_text("Kj-JD-Jz", "Укажите как минимум одного получателя.")
        self.assertTrue(mes)

    def test_dynamic_save(self):
        """
        Шаги:
        1) Заполнить любое поле (можно одним символом)
        2) Подождать пару секунд

        Ожидаемый результат:
        В нижней части формы отправки справа появится надпись: "Идет сохранение", а затем: "Сохранено".
        """
        self.driver.find_element_by_name("to").send_keys("а")
        mes = self.wait_text("aWQ", "Идет сохранение")
        self.assertTrue(mes)
        mes = self.wait_text("aWQ", "Сохранено")
        self.assertTrue(mes)

    def wait_text(self, name, text):
        return WW(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, name), text))

    def tearDown(self):
        self.driver.quit()



if __name__ == "__main__":
    unittest.main()

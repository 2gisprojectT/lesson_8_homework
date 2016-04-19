from unittest import TestCase
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SiteTestCase(TestCase):
    def setUp(self):
        """
            Начальные условия:
                1. Находиться на сайте 2gis.ru
        """
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.driver.get('https://2gis.ru')

        self.actions = ActionChains(self.driver)
        self.zoom = self.driver.find_element_by_class_name('zoom__inButton')
        self.map_element = self.driver.find_element_by_class_name('map')

    def inc_zoom(self, count):
        while count > 0:
            self.zoom.click()
            count -= 1

    def test_click_district(self):
        """
            Test Case:
                Проверка отображения информации о Центральном округе по клику на карте
            Шаги:
                1. Кликнуть по любым координатам Центрального округа
            Ожидаемый результат:
                Всплывет карточка Центрального округа с соответствующим названием
        """
        self.actions.move_to_element_with_offset(self.map_element, 950, 300).click().perform()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'callout__headerTitle')))
        district_text = self.driver.find_element_by_class_name('callout__headerTitle').text
        self.assertEqual(district_text, 'Центральный округ')

    def test_click_object_with_zoom(self):
        """
            Test Case:
                Проверка отображения информации о Первомайском сквере после увеличения зума карты
            Шаги:
                1. Приблизить карту минимум 4 раза
                2. Кликнуть по любым координатам Первомайского сквера
            Ожидаемый результат:
                Всплывет карточка Первомайского сквера с соответствующим названием
        """
        self.inc_zoom(4)
        self.actions.move_to_element_with_offset(self.map_element, 1100, 270).click().perform()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'callout__headerTitle')))
        click_object_text = self.driver.find_element_by_class_name('callout__headerTitle').text
        self.assertEqual(click_object_text, 'Первомайский сквер')

    def test_click_object_and_search(self):
        """
            Test Case:
                Сравнение информации всплывающего окна организации и карточки организации после поиска
            Шаги:
                1. Приблизить карту минимум 4 раза
                2. Кликнуть по любым координатам Оперного театра
                3. В поисковой строке ввести: "Оперный театр"
                4. Кликнуть по первому результату поиска
            Ожидаемый результат:
                Название организации на карточке после поиска и на всплывающем окне совпадет
        """
        self.inc_zoom(4)
        self.actions.move_to_element_with_offset(self.map_element, 1250, 210).click().perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'callout__headerTitle')))
        click_object_text = self.driver.find_element_by_class_name('callout__headerTitle').text

        self.driver.find_element_by_class_name('suggest__input').send_keys('Оперный театр')
        self.driver.find_element_by_class_name('searchBar__submit').click()
        self.driver.find_element_by_class_name('miniCard__headerTitleLink').click()
        search_object_text = self.driver.find_element_by_class_name('cardHeader__headerNameText').text

        self.assertEqual(('' + click_object_text).lower(), ('' + search_object_text).lower())

    def test_click_object_and_entrance(self):
        """
            Test Case:
                Проверка отображаемой информации на карточке после нажатия на кнопку "Найти вход"
            Шаги:
                1. Приблизить карту минимум 4 раза
                2. Кликнуть по любым координатам Оперного театра
                3. Кликнуть по кнопке "Найти вход"
            Ожидаемый результат:
                Всплывшее окно организации на карте пропадет
                На карте стрелочкой будет показан вход в здание
                Отобразится карточка организации Оперный театр с соответствующим названием
        """
        self.inc_zoom(4)
        self.actions.move_to_element_with_offset(self.map_element, 1250, 210).click().perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'callout__headerTitle')))
        click_object_text = self.driver.find_element_by_class_name('callout__headerTitle').text

        self.driver.find_element_by_class_name('callout__entrance').click()
        entrance_object_text = self.driver.find_element_by_class_name('geoCard2__name').text

        self.assertEqual(click_object_text, entrance_object_text)

    def test_click_object_and_details(self):
        """
            Test Case:
                Проверка отображаемой информации на карточке после нажатия на кнопку "Узнать больше"
            Шаги:
                1. Приблизить карту минимум 4 раза
                2. Кликнуть по любым координатам Оперного театра
                3. Кликнуть по кнопке "Узнать больше"
            Ожидаемый результат:
                Всплывшее окно организации на карте пропадет
                Отобразится карточка организации Оперный театр с соответствующим названием
        """
        self.inc_zoom(4)
        self.actions.move_to_element_with_offset(self.map_element, 1250, 210).click().perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'callout__headerTitle')))
        click_object_text = self.driver.find_element_by_class_name('callout__headerTitle').text

        self.driver.find_element_by_class_name('callout__details').click()
        details_object_text = self.driver.find_element_by_class_name('geoCard2__name').text

        self.assertEqual(click_object_text, details_object_text)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

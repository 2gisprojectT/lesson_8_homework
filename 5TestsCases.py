from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class FiveTestsCases(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('http://2gis.ru/novosibirsk')
        self.driver.find_element_by_class_name('searchBar__buttons').click()
        self.search_bar_from_field = self.driver.find_element_by_css_selector("div[class='searchBar__textfield _from'] input[class='suggest__input']")
        self.search_bar_to_field = self.driver.find_element_by_css_selector("div[class='searchBar__textfield _to'] input[class='suggest__input']")

    def web_driver_wait(self, value, obj):
        WebDriverWait(self.driver, value).until(EC.element_to_be_clickable((By.CSS_SELECTOR, obj)))

    def zoom(self, value):
        zoom_button = self.driver.find_element_by_css_selector("div[class='zoom__button _type_in']")
        self.web_driver_wait(5, 'div[class="online__map"]')
        n = 0
        while n < value:
            self.web_driver_wait(5, 'div[class="online__map"]')
            zoom_button.click()
            n += 1

    def test_search_good_date_input(self):
        """Тест Кейс1:
            Проверка поиска указанного маршрута
            Предусловия:
            1. Доступ в интернет
            2. Перейти на сайте 2gis.ru/novosibirsk в firefox
            3. Выбрать пункт "Проезд"
            Шаги:
            1. Ввести в поле "Откуда" название/адрес реального объекта
            2. Ввести в поле "Куда" название/адрес реального объекта
            3. Нажать enter
            Ожидаемый результат: Маршрут найден
        """
        obj1 = 'Площадь Кирова'
        obj2 = 'Версаль'
        self.web_driver_wait(5, ".searchBar__formsIn")
        self.search_bar_from_field.send_keys(obj1)
        self.search_bar_to_field.send_keys(obj2)
        self.search_bar_to_field.submit()
        rout_list = self.driver.find_element_by_css_selector(".routeResults")
        self.assertTrue(obj1 and obj2 in rout_list.text)

    def test_search_bad_date_input(self):
        """Тест Кейс2:
            Проверка поиска указанного маршрута
            Предусловия:
            1. Доступ в интернет
            2. Перейти на сайте 2gis.ru/novosibirsk в firefox
            3. Выбрать пункт "Проезд"
            Шаги:
            1. Ввести в поле "Откуда" название/адрес несуществующего объекта (Пример: апрпар)
            2. Ввести в поле "Куда" название/адрес несуществующего объекта (Пример: врпрпавп)
            3. Нажать enter
            Ожидаемый результат:
            Появилась панель: “Увы, невозможно построить такой маршрут”
        """
        obj1 = 'алллаитл'
        obj2 = 'лрдод'
        self.web_driver_wait(5, ".searchBar__formsIn")
        self.search_bar_from_field.send_keys(obj1)
        self.search_bar_to_field.send_keys(obj2)
        self.search_bar_to_field.submit()
        self.assertTrue(self.driver.find_element_by_css_selector(".noResults__routeType"))

    def test_search_map_click_date_input(self):
        """Тест Кейс3:
            Проверка поиска указанного маршрута кликом по карте
            Предусловия:
            1. Доступ в интернет
            2. Перейти на сайте 2gis.ru/novosibirsk в firefox
            3. Выбрать пункт "Проезд"
            Шаги:
            1. Приблизте карту, чтобы на ней появились объекты
            2. Кликните на первое место/объект откуда строить маршрут
            3. Кликните на второе место/объект куда строить маршрут
            Ожидаемый результат:
            Появилась панель: Маршрут найден
        """
        from_obj = "img[src='http://tile0.maps.2gis.com/tiles?x=47857&y=20719&z=16&v=1']"
        to_obj = "img[src='http://tile2.maps.2gis.com/tiles?x=47858&y=20720&z=16&v=1']"
        self.zoom(5)
        self.web_driver_wait(5, from_obj)
        self.driver.find_element_by_css_selector(from_obj).click()
        self.web_driver_wait(5, ".map__markerRouteSearchPin")
        self.driver.find_element_by_css_selector(to_obj).click()
        self.assertTrue(self.driver.find_element_by_css_selector("path[class='routeSearchGeometry leaflet-interactive']").is_displayed())

    def test_search_from_different_objects(self):
        """Тест Кейс4:
            Проверка поиска указанного маршрута для вида транспорта "Автомобильный маршрут"
            Предусловия:
            1. Доступ в интернет
            2. Перейти на сайте 2gis.ru/novosibirsk в firefox
            3. Выбрать пункт "Проезд"
            Шаги:
            1.  Выбрать вид транспорта "Автомобильный маршрут"
            1.	Ввести в поле "Откуда" адрес реального здания
            2.	Ввести в поле "Куда" название реальной остановки (Пример: Телецентр Остановка)
            3.	Нажать кнопку "Найти"

            Ожидаемый результат: Указанный маршрут построен
        """
        obj1 = 'Виктора Уса 9'
        obj2 = 'Телецентр Остановка'
        self.driver.find_element_by_css_selector(".searchBar__transportCar").click()
        self.search_bar_from_field.send_keys(obj1)
        self.search_bar_to_field.send_keys(obj2)
        self.search_bar_to_field.submit()
        rout_list = self.driver.find_element_by_css_selector(".autoResults")
        self.assertTrue(obj1 and obj2 in rout_list.text)

    def test_search_subway_option(self):
        """Тест Кейс5:
            Проверка поиска указанного маршрута от станции метро до станции метро
            Предусловия:
            1. Доступ в интернет
            2. Установленный браузер последней версии Google Chrome
            3. Перейти на сайте 2gis.ru/novosibirsk в firefox
            4. Выбрать пункт "Проезд"
            5. Выбрать вид транспорта Метро
            Шаги:
            1.	Ввести в поле "Откуда" название реальной станции метро (Пример: Студенческая)
            2.	Ввести в поле "Куда" название другой реальной станции метро (Пример: Площадь Маркса)
            3.	Нажать кнопку "Найти"
            Ожидаемый результат: Маршрут найден
        """
        obj1 = 'Студенческая'
        obj2 = 'Маркса'
        self.driver.find_element_by_css_selector(".searchBar__transportSubway").click()
        self.search_bar_from_field.send_keys(obj1)
        self.search_bar_to_field.send_keys(obj2)
        self.driver.find_element_by_css_selector(".searchBar__submit._rs").click()
        rout_list = self.driver.find_element_by_css_selector(".routeResults")
        self.assertTrue(obj1 and obj2 in rout_list.text)

    def tearDown(self):
        self.driver.quit()

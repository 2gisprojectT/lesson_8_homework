from unittest import TestCase
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class FiveTestsCases(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('http://2gis.ru/novosibirsk')
        self.driver.find_element_by_class_name('searchBar__buttons').click()

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
        from_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-2']/..//input[@class='suggest__input']")
        from_field.send_keys('Площадь Кирова')
        to_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-3']/..//input[@class='suggest__input']")
        to_field.send_keys('Версаль')
        to_field.submit()
        rout_list = self.driver.find_element_by_xpath("//div[@class='routeResults__wrap']")
        self.assertTrue('Площадь Кирова' and 'Площадь Кирова' in rout_list.text)

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
        from_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-2']/..//input[@class='suggest__input']")
        from_field.send_keys('алллаитл')
        to_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-3']/..//input[@class='suggest__input']")
        to_field.send_keys('лрдод')
        to_field.submit()
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='noResults__scroller _scrollbar']"))

    def test_search_map_click_date_input(self):
        """Тест Кейс3:
            Проверка поиска указанного маршрута
            Предусловия:
            1. Доступ в интернет
            2. Перейти на сайте 2gis.ru/novosibirsk в firefox
            3. Выбрать пункт "Проезд"
            Шаги:
            1. Выберете первое здание на карте откуда строить маршрут
            2. Нажмите кнопку "Путь отсюда" на появившейся инф. панели выбранного объекта
            3. Выберете второе здание на карте куда строить маршрут
            4. Нажмите кнопку "сюда" на появившейся инф. панели выбранного объекта
            Ожидаемый результат:
            Появилась панель: Маршрут найден
        """
        zoom_button = self.driver.find_element_by_xpath("//div[@class='zoom__eventArea zoom__inButton']")
        n = 0
        while n < 5:
            time.sleep(1)
            zoom_button.click()
            n += 1
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//img[@src='http://tile0.maps.2gis.com/tiles?x=47857&y=20719&z=16&v=1']")))
        from_field = self.driver.find_element_by_xpath("//img[@src='http://tile0.maps.2gis.com/tiles?x=47857&y=20719&z=16&v=1']")
        from_field.click()
        time.sleep(1)
        to_field = self.driver.find_element_by_xpath("//img[@src='http://tile2.maps.2gis.com/tiles?x=47858&y=20720&z=16&v=1']")
        to_field.click()
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='map__markerRouteSearch  _type_afoot _city_novosibirsk']/..//div[@class='map__markerRouteSearchPin']").is_displayed())
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='map__markerRouteSearch _end  _type_afoot _city_novosibirsk']/..//div[@class='map__markerRouteSearchPin']").is_displayed())
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='leaflet-pane leaflet-route-pane']").is_displayed())

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
        car_button = self.driver.find_element_by_xpath("//div[@class='searchBar__transportButton searchBar__transportCar']")
        car_button.click()
        from_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-2']/..//input[@class='suggest__input']")
        from_field.send_keys('Виктора Уса 9')
        to_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-3']/..//input[@class='suggest__input']")
        to_field.send_keys('Телецентр Остановка')
        to_field.submit()
        rout_list = self.driver.find_element_by_xpath("//div[@class='autoResults__wrap']")
        self.assertTrue('Виктора Уса 9' and 'Телецентр Остановка' in rout_list.text)

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
        subway_button = self.driver.find_element_by_xpath("//div[@class='searchBar__transportButton searchBar__transportSubway']")
        subway_button.click()
        from_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-2']/..//input[@class='suggest__input']")
        from_field.send_keys('Студенческая')
        to_field = self.driver.find_element_by_xpath("//div[@id='module-1-1-3']/..//input[@class='suggest__input']")
        to_field.send_keys('Площадь Маркса')
        search_button = self.driver.find_element_by_xpath("//button[@class='searchBar__submit _rs']")
        search_button.click()
        rout_list = self.driver.find_element_by_xpath("//div[@class='routeResults__wrap']")
        self.assertTrue('Студенческая' and 'Площадь Маркса' in rout_list.text)

    def tearDown(self):
        self.driver.quit()

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dict_enums import ElementCondition
from selenium.webdriver.common.keys import Keys
from random import choice
import logging
import allure


class BasePage:
    def __init__(self, browser, default_timeout: int = 5):
        self.browser = browser
        self.default_timeout = default_timeout

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Инициализация страницы {self.__class__.__name__}")

        self.conditions = {
            ElementCondition.VISIBLE: EC.visibility_of_element_located,
            ElementCondition.PRESENT: EC.presence_of_element_located,
            ElementCondition.INVISIBLE: EC.invisibility_of_element_located,
        }

    def _get_timeout(self, timeout: int or None):
        return timeout if timeout is not None else self.default_timeout

    def _get_wait(self, timeout: int or None):
        wait_time = self._get_timeout(timeout)
        return WebDriverWait(self.browser, wait_time)

    def wait_element_for_condition(self, locator: tuple, condition: ElementCondition, element_name: str | None,
                                   timeout: int | None):
        """
        Ожидает выполнения условия для элемента
        """

        element_label = element_name or str(locator)
        wait = self._get_wait(timeout)
        actual_time = self._get_timeout(timeout)

        self.logger.debug(f"Ожидание элемента {element_label} с условием {condition.value}")

        try:
            ec_condition = self.conditions[condition]
            result = wait.until(
                ec_condition(locator)
            )
            self.logger.info(f"Элемент {element_label} успешно найден")
            return result

        except TimeoutException:
            self.logger.error(f"Элемент '{element_label}' не стал {condition.value} в течение {actual_time} секунд")
            assert False, (
                f"Элемент '{element_label}' не стал {condition.value} в течение {actual_time} секунд"
            )

    @allure.step("Проверка видимости элемента: {locator}")
    def assert_element_visible(self, locator: tuple, element_name: str = None, timeout: int = None):
        element_label = element_name or str(locator)
        self.logger.info(f"Проверка видимости элемента: {element_label}")

        element = self.wait_element_for_condition(
            locator,
            ElementCondition.VISIBLE,
            element_name,
            timeout
        )

        self.logger.debug(f"Элемент {element_label} видим")
        assert element.is_displayed(), (
            f"Элемент '{element_label}' найден, но не отображается на странице"
        )

    @allure.step("Проверка невидимости элемента: {locator}")
    def assert_element_invisible(self, locator: tuple, element_name: str = None, timeout: int = None):
        element_label = element_name or str(locator)

        is_invisible = self.wait_element_for_condition(
            locator,
            ElementCondition.INVISIBLE,
            element_name,
            timeout
        )

        assert is_invisible, (
            f"Элемент '{element_label}' все ещё отображается на странице"
        )

    @allure.step("Проверка присутствия элемента на странице: {locator}")
    def assert_element_present(self, locator: tuple, element_name: str = None, timeout: int = None):
        element_label = element_name or str(locator)

        element = self.wait_element_for_condition(
            locator,
            ElementCondition.PRESENT,
            element_name,
            timeout
        )
        assert element, (
            f"Элемент '{element_label}' отсутствует"
        )

    @allure.step("Поиск всех элементов: {locator}")
    def find_all_elements(self, locator):
        return self.browser.find_elements(*locator)

    def get_all_element_values(self, locator):
        elements = self.find_all_elements(locator)
        values_list = []

        for element in elements:
            values_list.append(element.text)

        return values_list

    @allure.step("Получение видимого элемента: {locator}")
    def get_visible_element(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(locator, ElementCondition.VISIBLE, element_name, timeout)
        return element

    @allure.step("Получение представленного на странице элемента: {locator}")
    def get_present_element(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(locator, ElementCondition.PRESENT, element_name, timeout)
        return element

    @allure.step("Клик по случайному элементу")
    def click_on_random_element(self, elements):
        random_element = choice(elements)
        self.logger.info("Клик по случайному элементу")
        random_element.click()

    @allure.step("Очистка поля и ввод значения")
    def clear_and_send_keys(self, element, keys):
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.DELETE)
        element.send_keys(keys)

    @allure.step("Клик по всем элементам списка")
    def click_on_all_elements(self, elements):
        self.logger.info(f"Клик по {len(elements)} элементам")
        for element in elements:
            element.click()

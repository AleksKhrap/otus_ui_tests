from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dict_enums import ElementCondition
from selenium.webdriver.common.keys import Keys
from random import choice


class BasePage:
    def __init__(self, browser, default_timeout: int = 5):
        self.browser = browser

        self.default_timeout = default_timeout

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

    def wait_element_for_condition(self, locator: tuple, condition: ElementCondition, element_name: str or None,
                                   timeout: int or None):
        """
        Ожидает выполнения условия для элемента
        """

        element_label = element_name or str(locator)
        wait = self._get_wait(timeout)
        actual_time = self._get_timeout(timeout)

        try:
            ec_condition = self.conditions[condition]
            result = wait.until(
                ec_condition(locator)
            )
            return result

        except TimeoutException:
            assert False, (
                f"Элемент '{element_label}' не стал {condition.value} в течение {actual_time} секунд"
            )

    def assert_element_visible(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(
            locator,
            ElementCondition.VISIBLE,
            element_name,
            timeout
        )

        assert element.is_displayed(), (
            f"Элемент '{element_name or str(locator)}' найден, но не отображается на странице"
        )

    def assert_element_invisible(self, locator: tuple, element_name: str = None, timeout: int = None):
        is_invisible = self.wait_element_for_condition(
            locator,
            ElementCondition.INVISIBLE,
            element_name,
            timeout
        )

        assert is_invisible, (
            f"Элемент '{element_name or str(locator)}' все ещё отображается на странице"
        )

    def assert_element_present(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(
            locator,
            ElementCondition.PRESENT,
            element_name,
            timeout
        )
        assert element, (
            f"Элемент '{element_name or str(locator)}' отсутствует"
        )

    def find_all_elements(self, locator):
        return self.browser.find_elements(*locator)

    def get_all_element_values(self, locator):
        elements = self.find_all_elements(locator)
        values_list = []

        for element in elements:
            values_list.append(element.text)

        return values_list

    def get_visible_element(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(locator, ElementCondition.VISIBLE, element_name, timeout)
        return element

    def get_present_element(self, locator: tuple, element_name: str = None, timeout: int = None):
        element = self.wait_element_for_condition(locator, ElementCondition.PRESENT, element_name, timeout)
        return element

    @staticmethod
    def click_on_random_element(elements):
        random_element = choice(elements)
        random_element.click()

    @staticmethod
    def clear_and_send_keys(element, keys):
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.DELETE)
        element.send_keys(keys)

    @staticmethod
    def click_on_all_elements(elements):
        for element in elements:
            element.click()

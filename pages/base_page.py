from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dict_enums import ElementCondition


class BasePage:
    def __init__(self, browser, timeout: int = 5):
        self.browser = browser

        self.timeout = timeout
        self.wait = WebDriverWait(browser, timeout)

        self.conditions = {
            ElementCondition.VISIBLE: EC.visibility_of_element_located,
            ElementCondition.PRESENT: EC.presence_of_element_located,
            ElementCondition.INVISIBLE: EC.invisibility_of_element_located,
        }

    def wait_element_for_condition(self, locator: tuple, condition: ElementCondition, element_name: str or None):
        """
        Проверяет, что элемент отображается/отсутствует на странице.
        """

        element_label = element_name or str(locator)

        try:
            ec_condition = self.conditions[condition]
            element = self.wait.until(
                ec_condition(locator)
            )
            return element, element_label

        except TimeoutException:
            assert False, (
                f"Элемент '{element_label}' не стал {condition.value} в течение {self.timeout} секунд"
            )

    def assert_element_visible(self, locator: tuple, element_name: str = None):
        element, element_label = self.wait_element_for_condition(locator, ElementCondition.VISIBLE, element_name)

        assert element.is_displayed(), (
            f"Элемент '{element_label}' найден, но не отображается на странице"
        )

        return element

    def assert_element_invisible(self, locator: tuple, element_name: str = None):
        element, element_label = self.wait_element_for_condition(locator, ElementCondition.INVISIBLE, element_name)

        if not element.is_displayed():
            assert True, (
                f"Элемент '{element_label}' все ещё отображается на странице"
            )

        return element

    def assert_element_present(self, locator: tuple, element_name: str = None):
        element, element_label = self.wait_element_for_condition(locator, ElementCondition.PRESENT, element_name)
        return element

    def find_all_elements(self, locator):
        return self.browser.find_elements(*locator)

    def get_all_element_values(self, locator):
        elements = self.find_all_elements(locator)
        values_list = []

        for element in elements:
            values_list.append(element.text)

        return values_list

    def set_timeout(self, timeout):
        self.timeout = timeout
        self.wait = WebDriverWait(self.browser, self.timeout)
        return self.wait

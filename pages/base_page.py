from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, browser, timeout: int = 3):
        self.browser = browser

        self.timeout = timeout
        self.wait = WebDriverWait(browser, timeout)

    def assert_element_visible(self, locator: tuple, element_name: str = None):
        """
        Проверяет, что элемент отображается на странице.
        """

        element_label = element_name or str(locator)

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            assert element.is_displayed(), (
                f"Элемент '{element_label}' найден, но не отображается на странице"
            )

            return element

        except TimeoutException:
            assert False, (
                f"Элемент '{element_label}' не стал видимым в течение {self.timeout} секунд"
            )

    def find_all_elements(self, locator):
        return self.browser.find_elements(*locator)

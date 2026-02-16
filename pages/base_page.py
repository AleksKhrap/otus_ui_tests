from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    PRICES = (By.XPATH, '//*[@class="price"]')
    CURRENCY_BUTTON = (By.XPATH, '//button[@data-toggle="dropdown"]')
    DOLLAR = (By.XPATH, '//*[@title="US Dollar"]')

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def get_prices(self, prices, currency_button, dollar):
        initial_prices = self.browser.find_elements(*prices)
        initial_price_list = [price.text.strip().replace('€', '').replace(',', '') for price in initial_prices]

        self.browser.find_element(*currency_button).click()
        WebDriverWait(self.browser, 3).until(EC.visibility_of_element_located(dollar)).click()

        new_prices = self.browser.find_elements(*prices)
        new_price_list = [price.text.strip().replace('$', '').replace(',', '') for price in new_prices]

        return initial_price_list, new_price_list

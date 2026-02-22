from selenium.webdriver.common.by import By

PRICES = (By.XPATH, '//*[@class="price"]')
CURRENCY_BUTTON = (By.XPATH, '//button[@data-toggle="dropdown"]')
DOLLAR = (By.XPATH, '//*[@title="US Dollar"]')

def open_page(page, url):
    page.browser.get(url)

def get_prices(page):
    initial_prices = page.find_all_elements(PRICES)
    initial_price_list = [price.text.strip().replace('€', '').replace(',', '') for price in initial_prices]

    page.assert_element_visible(CURRENCY_BUTTON).click()
    page.assert_element_visible(DOLLAR).click()

    new_prices = page.find_all_elements(PRICES)
    new_price_list = [price.text.strip().replace('$', '').replace(',', '') for price in new_prices]

    return initial_price_list, new_price_list

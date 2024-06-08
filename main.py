import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class OpenCart:
    def __init__(self, driver):
        self.driver = driver

    def open_home_page(self):
        self.driver.get('https://demo.opencart-ru.ru/index.php?route=common/home')
        time.sleep(1.5)

    def click_on(self, by, locator):
        element = self.driver.find_element(by, locator)
        element.click()
        time.sleep(1.5)

    def enter_text(self, by, locator, text):
        element = self.driver.find_element(by, locator)
        element.send_keys(text)
        time.sleep(0.5)

    def choose_option_by_value(self, by, locator, value):
        element = self.driver.find_element(by, locator)
        element.click()
        time.sleep(0.5)
        option = self.driver.find_element(By.XPATH, f"//option[@value='{value}']")
        option.click()
        time.sleep(0.5)

    def navigate_back(self):
        self.driver.back()
        time.sleep(1.5)

@pytest.fixture
def driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--start-maximized')
    driver_instance = webdriver.Firefox(options=firefox_options)
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def opencart(driver):
    return OpenCart(driver)

@allure.step("Click on element")
def step_click_on(page, by, locator):
    page.click_on(by, locator)

@allure.step("Enter text")
def step_enter_text(page, by, locator, text):
    page.enter_text(by, locator, text)

@allure.step("Select option by value")
def step_choose_option_by_value(page, by, locator, value):
    page.choose_option_by_value(by, locator, value)

@allure.step("Navigate back")
def step_navigate_back(page):
    page.navigate_back()

@allure.feature("Functionality Verification")
@allure.story("User Registration Testing")
def test_register_user(opencart):
    opencart.open_home_page()
    allure.attach(opencart.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
    step_click_on(opencart, By.XPATH, "//a[@title='Личный кабинет']")
    step_click_on(opencart, By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']//a[contains(text(),'Регистрация')]")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_email']", "timofey.it.hub@gmail.com")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_password']", "^09D_+$A8g@7F_6$FGHFD5_43#21hfg&%")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_confirm_password']", "^09D_+$A8g@7F_6$FGHFD5_43#21hfg&%")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_firstname']", "Timofey")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_lastname']", "Frolov")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_telephone']", "89931425465")
    step_choose_option_by_value(opencart, By.XPATH, "//select[@id='register_country_id']", "432")
    step_choose_option_by_value(opencart, By.XPATH, "//select[@id='register_zone_id']", "32")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_city']", "Москва")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_postcode']", "14422")
    step_enter_text(opencart, By.XPATH, "//input[@id='register_address_1']", "Тополя")
    step_click_on(opencart, By.XPATH, "//a[@id='simpleregister_button_confirm']")

if __name__ == "__main__":
    pytest.main(args=['-s', '--alluredir', 'allure-results'])

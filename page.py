from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import data

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Chamar um táxi")]')

    def __init__(self, driver):
        self.driver = driver

    def _wait_for_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def _wait_for(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_call_taxi()

    def set_from(self, from_address):
        self._wait_for_visible(self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self._wait_for_visible(self.to_field).send_keys(to_address)

    def get_from(self):
        return self._wait_for(self.from_field).get_property('value')

    def get_to(self):
        return self._wait_for(self.to_field).get_property('value')

    def click_call_taxi(self):
        self._wait_for_visible(self.call_taxi_button).click()

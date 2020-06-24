from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    ADD_PERSONAL_ACCOUNT_BUTT = (By.XPATH, "//button[contains(text(), 'Add a personal account')]")

    def is_loaded(self):
        return self.wait_for_element_visibility(self.ADD_PERSONAL_ACCOUNT_BUTT).is_displayed()

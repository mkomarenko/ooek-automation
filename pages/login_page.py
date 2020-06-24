from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    url = 'https://ooek.od.ua/user/'

    LOGIN_INPUT = (By.ID, "id_username")
    PASSWORD_INPUT = (By.ID, "id_password")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Log in']")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[@class='close']")

    def do_login(self, credentials):
        self.wait_for_element_visibility(self.CLOSE_MODAL_BUTTON).click()
        login = self.wait_until_element_is_clickable(self.LOGIN_INPUT)
        login.send_keys(credentials[0])
        password = self.wait_for_element_visibility(self.PASSWORD_INPUT)
        password.send_keys(credentials[1])
        self.wait_for_element_visibility(self.SUBMIT_BUTTON).click()
        self.wait_for_element_visibility(self.CLOSE_MODAL_BUTTON).click()



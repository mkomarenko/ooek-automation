import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.home_page import HomePage

logger = logging.getLogger("app")


class LoginPage(BasePage):
    LOGIN_INPUT = (By.ID, "id_username")
    PASSWORD_INPUT = (By.ID, "id_password")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Log in']")
    DO_NOT_SHOW_AGAIN_BUTTON_1 = (By.XPATH, "//button[@id='infouser' and not(@disabled)]")
    DO_NOT_SHOW_AGAIN_BUTTON_2 = (By.XPATH, "//button[@id='modal-yes' and not(@disabled)]")
    DO_NOT_SHOW_AGAIN_BUTTON_3 = (By.XPATH, "//button[@id='infouserlsch' and not(@disabled)]")
    OVERLAY_1 = (By.ID, "exampleinfouser")
    OVERLAY_2 = (By.ID, "exampleModalScrollablee")

    def is_loaded(self) -> bool:
        """
        Checks whether Login page is loaded
        :return: True if login and password fields are displayed, False otherwise
        """
        try:
            fields_are_displayed = self.wait_for_element_visibility(self.LOGIN_INPUT).is_displayed() and \
                                   self.wait_for_element_visibility(self.PASSWORD_INPUT).is_displayed()
            return fields_are_displayed
        except TimeoutException:
            return False

    def login_with_credentials(self, username: str, password: str) -> HomePage:
        """
        Login to personal account
        :param username: user login
        :param password: user password
        :return: Home page
        """
        do_not_show_button = self.wait_for_element_visibility(self.DO_NOT_SHOW_AGAIN_BUTTON_1)
        do_not_show_button.click()
        logger.info("Clicking 'Do not show again' button on Login page opening")
        try:
            self.wait_until_element_invisible(self.OVERLAY_1)
        except TimeoutException:
            logger.warning("Dialog was not closed at first time. "
                           "Clicking 'Do not show again' button on Login page opening 1 more time")
            do_not_show_button.click()
            self.wait_until_element_invisible(self.OVERLAY_1)

        login_el = self.wait_until_element_is_clickable(self.LOGIN_INPUT)
        login_el.clear()
        login_el.send_keys(username)
        password_el = self.wait_until_element_is_clickable(self.PASSWORD_INPUT)
        password_el.clear()
        password_el.send_keys(password)
        self.wait_for_element_visibility(self.SUBMIT_BUTTON).click()

        do_not_show_button_2 = self.wait_for_element_visibility(self.DO_NOT_SHOW_AGAIN_BUTTON_2)
        logger.info("Clicking 'Do not show again' button after login")
        do_not_show_button_2.click()
        try:
            self.wait_until_element_invisible(self.OVERLAY_2)
        except TimeoutException:
            logger.warning("Dialog was not closed at first time. "
                           "Clicking 'Do not show again' button after login 1 more time")
            do_not_show_button_2.click()
            self.wait_until_element_invisible(self.OVERLAY_2)

        self.wait_until_element_is_clickable(self.DO_NOT_SHOW_AGAIN_BUTTON_3).click()
        return HomePage(self.driver)

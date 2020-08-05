import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.my_accounts_page import MyAccountsPage

logger = logging.getLogger('ooek-e2e')


class AddAccountPage(BasePage):
    PERSONAL_INVOICE_INPUT = (By.ID, "id_lsch")
    SUBMIT_PERSONAL_ACCOUNT_BTN = (By.ID, "getRequest")

    def is_loaded(self) -> bool:
        """
        Checks if the page was loaded
        :return: True if page was loaded, False otherwise
        """
        return self.wait_for_element_visibility(self.SUBMIT_PERSONAL_ACCOUNT_BTN).is_displayed()

    def enter_personal_account(self, value: str) -> None:
        """
        Enter personal invoice on add personal account form
        :param value: personal invoice in the format *****/*******
        :return: None
        """
        element = self.wait_until_element_is_clickable(self.PERSONAL_INVOICE_INPUT)
        logger.info("Enter personal account number: {}".format(value))
        element.send_keys(value)

    def click_submit_a_personal_account(self) -> MyAccountsPage:
        """
        Click submit button on Add a Personal Account form
        :return: My Accounts page
        """
        self.wait_until_element_is_clickable(self.SUBMIT_PERSONAL_ACCOUNT_BTN).click()
        return MyAccountsPage(self.driver)

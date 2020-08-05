import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.add_account_page import AddAccountPage
from pages.base_page import BasePage
from pages.my_accounts_page import MyAccountsPage

logger = logging.getLogger('ooek-e2e')


class HomePage(BasePage):
    FORM_SECTION = (By.CLASS_NAME, ".form-section")
    HOUSEHOLD_CLIENT_TAB = (By.ID, "pills-home-tab")
    ADD_PERSONAL_ACCOUNT_CARD = (By.XPATH, "//a[@href='https://ooek.od.ua/profile1/']/div[@class='service']")
    MY_ACCOUNTS_CARD = (By.XPATH, "//a[@href='https://ooek.od.ua/score/']/div[@class='service']")

    def is_loaded(self) -> bool:
        """
        Checks whether the Home page is loaded
        :return: True if page was loaded, False otherwise
        """
        try:
            client_tab_displayed = self.wait_for_element_visibility(self.HOUSEHOLD_CLIENT_TAB).is_displayed()
            logger.debug("Client tab is displayed. Home page was successfully loaded")
            return client_tab_displayed
        except TimeoutException as e:
            logger.error("Client tab is not displayed. Home page may not be loaded. {}".format(str(e)))
            return False

    def click_add_a_personal_account_card(self) -> AddAccountPage:
        """
        Click Add Personal Account card on the household client menu
        :return: Add Account page
        """
        try:
            self.wait_until_element_is_clickable(self.ADD_PERSONAL_ACCOUNT_CARD).click()
            logger.info("Clicking 'Add Personal Account'")
            return AddAccountPage(self.driver)
        except TimeoutException as e:
            logger.error("Error while clicking 'Add Personal Account' card. ".format(str(e)))
            raise

    def click_my_accounts_card(self):
        """
        Click My Accounts card on the household client menu
        :return:  My Accounts page
        """
        try:
            self.wait_until_element_is_clickable(self.MY_ACCOUNTS_CARD).click()
            logger.info("Clicking 'My Accounts'")
            return MyAccountsPage(self.driver)
        except TimeoutException as e:
            logger.error("Error while clicking 'My Accounts' card. ".format(str(e)))
            raise

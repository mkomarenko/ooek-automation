import logging
from typing import List, Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage

logger = logging.getLogger("app")


class MyAccountsPage(BasePage):
    INVOICE_ALERT_INFO = (By.CLASS_NAME, "alert-info")
    MY_ACCOUNTS_TABLE_ROWS = (By.XPATH, "//div[@class='table-responsive-xl']/table/tbody/tr")
    CONFIRM_DELETE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button.btn-outline-danger")
    REMOVE_ACCOUNT_CONFIRM_MESSAGE = (By.XPATH, "//div[@class = 'form-section']/h2")

    def is_loaded(self) -> bool:
        """
        Checks if the page was loaded
        :return: True if page was loaded, False otherwise
        """
        return self.get_my_accounts_table_rows()[0].is_displayed()

    def get_success_invoice_alert_message(self) -> str:
        """
        Return success alert message that should appear after adding a new account
        :return: alert message
        """
        try:
            el = self.wait_for_element_visibility(self.INVOICE_ALERT_INFO)
            logger.info("Getting success alert message: {}".format(el.text))
            return el.text
        except TimeoutException:
            logger.error("Success alert message is not displayed")
            return ''

    def get_my_accounts_table_rows(self) -> List[WebElement]:
        """
        Method that retrieve all rows from my accounts table
        :return: list of WebElements
        """
        return self.find_elements_with_wait(self.MY_ACCOUNTS_TABLE_ROWS)

    def search_row_by_account_number(self, account_num: str) -> Union[WebElement, None]:
        """
        Method searches account in my accounts table by account number
        :param account_num: account number to search for
        :return: table row element if account is found, None otherwise
        """
        for row in self.get_my_accounts_table_rows():
            account_col_el = row.find_element(By.XPATH, "./td[1]")
            if account_col_el.text == account_num:
                logger.info("Found row with account number: {}".format(account_num))
                return row
        logger.warning("A row with a specified account number was not found")

    def press_remove_account(self, acc_number: str) -> None:
        """
        Click Remove button for account with a specified number in My Accounts table
        :param acc_number: account number to be removed
        :return: None
        """
        row = self.search_row_by_account_number(acc_number)

        if not row:
            logger.error("Account removal failed. Account with a specified number was not found")
            return

        remove_btn = row.find_element(By.XPATH, "./td/a[contains(@class, 'btn-danger')]")
        logger.info("Click Remove button for account: {}".format(acc_number))
        remove_btn.click()

    def get_remove_account_confirm_message(self) -> str:
        """
        Return confirmation message displayed when user tries to remove account
        :return: remove account confirmation message
        """
        try:
            el = self.wait_for_element_visibility(self.REMOVE_ACCOUNT_CONFIRM_MESSAGE)
            logger.info("Getting remove account confirm message: {}".format(el.text))
            return el.text
        except TimeoutException:
            logger.error("Remove account confirmation message is not displayed")
            return ''

    def confirm_remove_account(self) -> None:
        """
        Click 'Yes, delete' account button
        :return: None
        """
        self.wait_for_element_visibility(self.CONFIRM_DELETE_ACCOUNT_BUTTON).click()

from pages.home_page import HomePage
from tests.base_test import BaseTest


class TestAccount(BaseTest):
    ACCOUNT_NUM = '04002/2499622'

    def test_should_add_account(self, session):
        home_page = HomePage(session.driver)
        assert home_page.is_loaded()
        add_account_page = home_page.click_add_a_personal_account_card()
        assert add_account_page.is_loaded()
        add_account_page.enter_personal_account(self.ACCOUNT_NUM)
        my_accounts_page = add_account_page.click_submit_a_personal_account()
        expected_message = "Your invoice has been successfully added"
        assert my_accounts_page.get_success_invoice_alert_message() == expected_message

    def test_should_open_my_accounts(self, session):
        home_page = HomePage(session.driver)
        home_page.open(session.url)
        assert home_page.is_loaded()
        my_accounts_page = home_page.click_my_accounts_card()
        assert my_accounts_page.search_row_by_account_number(self.ACCOUNT_NUM)

    def test_should_remove_account(self, session):
        home_page = HomePage(session.driver)
        home_page.open(session.url)
        assert home_page.is_loaded()
        my_accounts_page = home_page.click_my_accounts_card()
        # assert my_accounts_page.is_loaded()
        my_accounts_page.press_remove_account(self.ACCOUNT_NUM)
        expected_message = "You really want to remove the contract from your account \"{}".format(self.ACCOUNT_NUM)
        assert expected_message in my_accounts_page.get_remove_account_confirm_message()
        my_accounts_page.confirm_remove_account()
        assert my_accounts_page.search_row_by_account_number(self.ACCOUNT_NUM) is None

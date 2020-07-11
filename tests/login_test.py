from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


class TestLogin(BaseTest):
    def test_should_login(self, driver, credentials):
        login_page = LoginPage(driver)
        login_page.open()
        home_page = login_page.do_login(credentials)
        assert home_page.is_loaded()

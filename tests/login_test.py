import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.base_test import BaseTest

# pytestmark = pytest.mark.skip("This test suite will be disabled until test categories are implemented")


class TestLogin(BaseTest):
    def test_should_login(self, session):
        login_page = LoginPage(session.driver)
        login_page.open(session.url)
        home_page = HomePage(session.driver)
        if login_page.is_loaded():
            home_page = login_page.login_with_credentials(session.username, session.password)
        assert home_page.is_loaded()

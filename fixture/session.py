from pages.login_page import LoginPage


class Session:

    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def login_if_required(self):
        """
        Login if redirected to Login page
        :return: None
        """
        login_page = LoginPage(self.driver)
        login_page.open(self.url)
        if login_page.is_loaded():
            login_page.login_with_credentials(self.username, self.password)

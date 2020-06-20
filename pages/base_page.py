from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):

    url = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.url)

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    def wait_for_element_visibility(self, locator: tuple, wait_time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))

    def wait_until_element_is_clickable(self, locator: tuple, wait_time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))

    def find_elements_with_wait(self, locator, wait_time=10):
        """
        Find elements by specified locator and wait
        :param tuple locator: strategy and locator
        :param int wait_time: wait time in seconds
        :return: list of elements
        """
        return WebDriverWait(self.driver, wait_time).until(EC.visibility_of_all_elements_located(locator))

import logging
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger("app")


class BasePage(object):

    def __init__(self, driver: WebDriver) -> None:
        self.logger = logging.getLogger("app")
        self.driver = driver

    def open(self, url) -> None:
        self.driver.get(url)
        logger.info("Open url: {}".format(url))

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def find_element(self, page: object, *strategy_and_locator: tuple) -> WebElement:
        """
        Find element on the page using provided locator
        :param page: current page
        :param strategy_and_locator: location strategy and locator
        :return: found element
        """
        try:
            element = self.driver.find_element(*strategy_and_locator)
            self.logger.info("Getting element data: {}".format(element))
            return element
        except NoSuchElementException:
            self.logger.error("Element not found. Page: {0}, Location strategy: {1}, Locator: {2}".
                              format(page.__class__.__name__, strategy_and_locator[0], strategy_and_locator[1]))
            raise

    def wait_for_element_visibility(self, locator: tuple, wait_time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))

    def wait_until_element_is_clickable(self, locator: tuple, wait_time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))

    def wait_until_element_invisible(self, locator: tuple, wait_time: int = 10) -> bool:
        return WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element_located(locator))

    def find_elements_with_wait(self, locator: tuple, wait_time: int = 10) -> List[WebElement]:
        """
        Find elements by specified locator and wait
        :param tuple locator: strategy and locator
        :param int wait_time: wait time in seconds
        :return: list of elements
        """
        return WebDriverWait(self.driver, wait_time).until(EC.visibility_of_all_elements_located(locator))

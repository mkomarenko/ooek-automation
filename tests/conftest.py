import logging
import logging.config

import pytest
from selenium.webdriver.chrome import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from fixture.session import Session


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default='',
        help="frontend url",
    )
    parser.addoption(
        "--username",
        action="store",
        default='',
        help="testing user login",
    )
    parser.addoption(
        "--password",
        action="store",
        default='',
        help="testing user password",
    )


def get_url(request):
    url = request.config.getoption('--url')
    if not url:
        raise ValueError("Pytest option 'url' is missing or empty. Please specify url like this: "
                         "--url=<url>")
    return url


def get_username(request):
    username = request.config.getoption('--username')
    if not username:
        raise ValueError("Pytest option 'username' is missing or empty. Please specify username like this: "
                         "--username=<user name>")
    return username


def get_password(request):
    password = request.config.getoption('--password')
    if not password:
        raise ValueError("Pytest option 'password' is missing or empty. Please specify password like this: "
                         "--password=<password>")
    return password


@pytest.yield_fixture(scope="module", autouse=True)
def get_driver():
    web_driver = webdriver.WebDriver(executable_path=ChromeDriverManager().install())
    yield web_driver
    web_driver.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def configure_logging():
    logging.config.fileConfig(fname='config/logging.ini')
    logging.getLogger('ooek-e2e')


@pytest.yield_fixture(scope="module", autouse=True)
def session(request, get_driver):
    driver = get_driver
    url = get_url(request)
    username = get_username(request)
    password = get_password(request)
    current_session = Session(driver, url, username, password)
    if not request.module.__name__ == 'tests.login_test':
        current_session.login_if_required()
    yield current_session

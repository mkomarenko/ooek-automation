import logging
import logging.config
import os

import pytest
from selenium.webdriver.chrome import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

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
    parser.addoption(
        "--driver",
        action="store",
        default='chrome',
        help="driver type",
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


def get_driver(request):
    driver = request.config.getoption('--driver')
    if not driver:
        raise ValueError("Pytest option 'driver' is missing or empty. Please specify driver like this:"
                         "--driver=<driver>")
    elif driver not in ['chrome', 'firefox']:
        raise ValueError('"{}" is not a supported driver type"'.format(driver))
    return driver


@pytest.yield_fixture
def browser(request):
    driver = get_driver(request)
    if driver == 'chrome':
        web_driver = webdriver.WebDriver(executable_path=ChromeDriverManager().install())
    elif driver == 'firefox':
        web_driver = webdriver.WebDriver(executable_path=GeckoDriverManager().install())
    else:
        raise ValueError('"{}" is not a supported driver type"'.format(driver))
    yield web_driver
    web_driver.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def configure_logging():
    log_dir = 'logs'
    # Create log directory if not exists
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.config.fileConfig(fname='config/logging.ini')

    logging.getLogger('ooek-e2e')


@pytest.yield_fixture(autouse=True)
def session(request, browser):
    url = get_url(request)
    username = get_username(request)
    password = get_password(request)

    current_session = Session(browser, url, username, password)
    if not request.module.__name__ == 'tests.login_test':
        current_session.login_if_required()
    yield current_session

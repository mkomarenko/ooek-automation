import json
import logging
import logging.config
import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from fixture.session import Session

CONFIG_PATH = 'config/config.json'
SUPPORTED_BROWSERS = ['chrome', 'firefox']
LOG_CONFIG = 'config/logging.ini'
LOGGER_NAME = 'ooek-e2e'


@pytest.fixture(scope='session')
def config():
    # Read the JSON config file and returns it as a parsed dict
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data


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
    elif driver not in SUPPORTED_BROWSERS:
        raise ValueError("Unknown driver '{}' provided. Supported drivers: ".format(driver, SUPPORTED_BROWSERS))
    return driver


@pytest.fixture(scope="session")
def config_browser(config):
    if 'browser' not in config:
        raise Exception("Config file does not contain \"browser\"")
    elif config['browser'] not in SUPPORTED_BROWSERS:
        raise ValueError("Unknown browser '{}' provided. Supported browser types: {}".format(config['browser'],
                                                                                             SUPPORTED_BROWSERS))
    return config['browser']


@pytest.yield_fixture(scope="session")
def web_driver(config_browser):
    if config_browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    elif config_browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise ValueError("'{}' is not a supported browser".format(config_browser))
    yield driver
    driver.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def configure_logging():
    log_dir = 'logs'
    # Create log directory if not exists
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.config.fileConfig(fname=LOG_CONFIG)

    logging.getLogger(LOGGER_NAME)


@pytest.yield_fixture(scope='session', autouse=True)
def session(request, web_driver):
    url = get_url(request)
    username = get_username(request)
    password = get_password(request)

    current_session = Session(web_driver, url, username, password)
    # if not request.module.__name__ == 'tests.login_test':
    current_session.login_if_required()
    yield current_session

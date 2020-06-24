import pytest
from selenium.webdriver.chrome import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.yield_fixture(scope="session", autouse=True)
def driver():
    web_driver = webdriver.WebDriver(executable_path=ChromeDriverManager().install())
    yield web_driver
    web_driver.quit()


def pytest_addoption(parser):
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


@pytest.fixture
def credentials(request):
    user = request.config.getoption('--username')
    password = request.config.getoption('--password')
    return user, password

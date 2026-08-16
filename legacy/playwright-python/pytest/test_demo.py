from playwright.sync_api import Page
import pytest

#--headed
#--baseurl https://www.saucedemo.com
#--browser
#--browser-channel
#--tracing on
#--tracing retain-on-failure
#https://trace.playwright.dev/
# playwright show-trace test-results\pytest-test-demo-py-test-saucelab-chromium\trace.zip

# @pytest.mark.skip_browser("chromium")
@pytest.mark.only_browser("chromium")
def test_positive(page:Page):
    page.goto("/")
    assert page.title() == "Swag Labs"

def test_negative(page:Page):
    page.goto("/inventory.html")
    assert page.inner_text('h3') == "Epic sadface: You can only access '/inventory.html' when you are logged in."

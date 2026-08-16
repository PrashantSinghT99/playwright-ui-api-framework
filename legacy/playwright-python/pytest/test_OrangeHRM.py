from playwright.sync_api import sync_playwright
import pytest

def test_login():
 with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    assert page.title()=="OrangeHRM"
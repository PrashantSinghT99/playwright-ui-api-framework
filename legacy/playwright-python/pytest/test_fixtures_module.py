# #module,function,class
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        yield browser
        browser.close()
      
        
@pytest.fixture(scope="function")
def page(browser):
    page=browser.new_page()
    yield page
    page.close()
    
    
def test_google(page):
    page.goto("https://google.com")
    assert "Google" == page.title()
    
def test_portfolio(page):
    page.goto("https://github-portfolio-pst99.vercel.app/")
    assert "My Portfolio" == page.title()
    

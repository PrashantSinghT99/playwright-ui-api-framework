import pytest
from playwright.sync_api import sync_playwright,Page

# @pytest.fixture(scope='class')
# def browser(request):
#     with sync_playwright() as p:
#         browser=p.chromium.launch(headless=False)
#         # Attach the browser instance to the test class
#         request.cls.browser=browser 
#         yield browser
#         browser.close()

# Define a fixture with function-level scope      
@pytest.fixture(scope='function')
def page(page:Page):
    yield page
    page.close()
    
    
# Use the 'browser' fixture for the following test class
@pytest.mark.usefixtures('page')
class Test_titleclass:
    def test_google(self,page):
        page.goto('https://google.com')
        assert 'Google' == page.title()
        
    def test_portfolio(self,page):
        page.goto('https://github-portfolio-pst99.vercel.app/')
        assert 'My Portfolio' == page.title()
        
    
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
    
@pytest.mark.parametrize('username, password',[('admin','admin'),('test','test')])    
def test_parameter(page,username,password):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.wait_for_selector('//input[@name="username"]').type(username)
    page.wait_for_selector('//input[@name="password"]').type(password)
    page.wait_for_selector('//button[@type="submit"]').click()
    page.wait_for_timeout(2000)
    error_msg=page.wait_for_selector('//p[text()="Invalid credentials"]').text_content()
    assert error_msg == "Invalid credentials"
    
    
    
products=[
    (2,3,6),
    (1,99,99),
    (0,99,0)
]
@pytest.mark.parametrize('a,b,product',products)
def test_multiplication(a,b,product):
    assert a*b==product
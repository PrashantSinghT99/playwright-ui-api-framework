from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://www.redbus.in/")
    
    my_cookies=context.cookies()
    
    print("BEFORE",my_cookies)
    
    new_cookies={'name': 'currency', 'value': 'USD', 'domain': 'www.redbus.in', 'path': '/', 'expires': 1718514734.138288, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}
    
    context.add_cookies([new_cookies])
    
    print("AFTER",my_cookies)
    
    context.clear_cookies()
    
    print("cookies are cleared")
    
    context.close()
    browser.close()
    

# Get all the cookies from page.
# my_cookies = page.context.cookies()

# Clearing all the cookies.
# page.context.clear_cookies()

# Setting new cookies to page.
# page.context.add_cookies([new_cookies])

# Taking screenshot and storing the path
#  page.screenshot(path='test.png',full_page=True)
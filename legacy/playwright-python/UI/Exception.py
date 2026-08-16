from playwright.sync_api import sync_playwright

# Store multiple elements using list

list=[]

with sync_playwright() as p:
    try:
        browser=p.chromium.launch(headless=False)
        context=browser.new_context()
        page=context.new_page()
        page.goto("https://the-internet.herokuapp.com/")  
        # page.query_selector("abc").click()
        list=page.query_selector_all("a")
        
        print(len(list))
        
        for i in list:
            print(i.text_content())
            print(i.get_attribute('href'))
    except Exception as e:
        print(str(e))
    finally:
        page.close()
        context.close()
        browser.close()
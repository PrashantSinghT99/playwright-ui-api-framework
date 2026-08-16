from playwright.sync_api import sync_playwright

#switching b/w Tabs
with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://demo.automationtesting.in/Windows.html")
    page.wait_for_selector("//button[text()='    click   ']").click()
    page.wait_for_timeout(3000)
    
    # get all Tabs
    total_pages=context.pages
    print(len(total_pages))

    for p in total_pages:
        print(p)
        
    print(page.title())
    
    newpage=total_pages[1]
    # switch to new Tabs
    newpage.bring_to_front()
    page.wait_for_timeout(3000)
    
    print(newpage.title())
    newpage.close()
    browser.close()
    




from playwright.sync_api import sync_playwright


def handleDialog(dialog):
        message=dialog.message
        print(message)
        dialog.accept()
       
        
with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        # page.goto("https://demo.automationtesting.in/Selectable.html")
        # page.goto("https://the-internet.herokuapp.com/hovers")
        page.goto("https://demo.guru99.com/test/simple_context_menu.html")
        # page.wait_for_timeout(2000)
        
        # hover
        
        page.wait_for_selector('(//img[@alt="User Avatar"])[1]').hover()
        
        #selecting multiple keys
        
        page.keyboard.press("Control+A",delay=100)
        
        
        page.on('dialog',lambda dialog:print(dialog.message))
        # double click
        page.dblclick('//button[text()="Double-Click Me To See Alert"]')
        
        #right click
        page.wait_for_selector('//span[text()="right click me"]').click(button='right')
        page.on('dialog',lambda dialog:handleDialog(dialog))
        page.wait_for_selector('//ul[@class="context-menu-list context-menu-root"]/li/span[text()="Edit"]').click()
         
        # page.wait_for_selector("//h1").click()
        # page.wait_for_selector("//h1").click(modifiers=["Shift"])

        # hover_validation=page.wait_for_selector('//h5[text()="name: user1"]').is_visible()
        # print(hover_validation)
        # assert hover_validation is True
        # page.wait_for_selector('//a[text()="Alerts"]').click()
        page.wait_for_timeout(2000)
        # run_before_unload=True
        page.close()
        browser.close()



# Mouse Actions
#     Hover the dropdown
#     page.wait_for_selector('//a[text()="SwitchTo"]').hover()
#   Click on element
#     page.wait_for_selector('//a[text()="SwitchTo"]').click()
#      Double Click
#     page.wait_for_selector('//a[text()="SwitchTo"]').dblclick()
#     Right on Element
#     page.wait_for_selector('//a[text()="SwitchTo"]').click(button="right")
#     Shift Click
#     page.wait_for_selector('//a[text()="SwitchTo"]').click(modifiers=["Shift"])

#    Keyboard
#     page.wait_for_selector('//a[text()="SwitchTo"]').press("A")
#    Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape,
# ArrowDown, End, Enter, Home, Insert, PageDown, PageUp, ArrowRight,
# ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc.
#     page.wait_for_selector('//a[text()="SwitchTo"]').press("$")
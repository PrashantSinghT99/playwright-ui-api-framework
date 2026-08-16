from playwright.sync_api import sync_playwright


def handleResponse(response):
    if 'https://www.plus2net.com/php_tutorial/dd-ajax.php?' in response.url:
        status=response.status
        data=response.json()
        print('status:',status,'data: ',data)
    

with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        context=browser.new_context()
        page=context.new_page()
        page.goto("https://www.plus2net.com/php_tutorial/ajax_drop_down_list-demo.php")
        page.locator('//select[@name="cat"]').select_option("3")
        page.on('response',lambda response:handleResponse(response))
        page.wait_for_timeout(2000)


# Identifying AJAX calls and their triggers
# Intercepting and inspecting AJAX requests and responses
# Extracting valuable data from AJAX responses
# Handling pagination and infinite scroll scenarios with AJAX
# Synchronizing actions with AJAX completion
        
        
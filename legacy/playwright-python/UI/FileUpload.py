# set_input_files
#download listen to download event and store using download.save_as("location")

from playwright.sync_api import sync_playwright

def handledownload(download):
    download_loc='./UI/test.png'
    download.save_as(download_loc)
    
    


# with sync_playwright() as p:
#     browser=p.chromium.launch(headless=False)
#     context=browser.new_context()
#     page=browser.new_page()
    
#     page.goto("https://demo.automationtesting.in/FileUpload.html")
    
#     file_loc="note.txt"
#     upload=page.query_selector('//input[@id="input-4"]')
    
#     upload.set_input_files(file_loc)
#     page.wait_for_timeout(4000)
    
with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    page=browser.new_page()
    
    page.goto("https://the-internet.herokuapp.com/download")
    
    page.on('download',handledownload)
    page.query_selector('//a[text()="puppy_and_kitten.jpg"]').click()
    
    page.wait_for_timeout(4000)
    
    
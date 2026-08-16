import asyncio
from playwright.async_api import async_playwright

#to store dialog message
text_alert=[]

async def handle_dialog(dialog):
    message = dialog.message
    text_alert.append(message)
    await dialog.accept("Prashant")
    
#accept

async def main():
   async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        await page.set_viewport_size({"width": 1800, "height": 1200})
        await page.goto("https://demo.automationtesting.in/Alerts.html")

        # Handle alert with OK and Cancel
        await page.click('a[href="#CancelTab"]')
        await page.wait_for_timeout(2000)

        #page.on('dialog',lambda dialog:dialog.accept())
        page.on('dialog',lambda dialog:handle_dialog(dialog))
        # page.on('dialog',lambda dialog:print(dialog.message))
        await page.click('button[class="btn btn-primary"]')
        
        validate_msg = await page.text_content('//div[@id="CancelTab"]/p')

        await page.wait_for_timeout(2000)
        assert validate_msg == "You pressed Ok", f"Expected 'You pressed Ok', but got '{validate_msg}'"
        #You Pressed Cancel
        print(text_alert[0])
        await context.tracing.stop(path="logs/dialogs.zip")
        await browser.close()


#dismiss

async def cancel():
   async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1800, "height": 1200})
        await page.goto("https://demo.automationtesting.in/Alerts.html")

        #steps performed
        
        await page.click('a[href="#CancelTab"]')
        await page.wait_for_timeout(2000)
        
        page.on('dialog',lambda dialog:dialog.dismiss())
        await page.click('button[class="btn btn-primary"]')
        
        #assertions
        validate_msg = await page.text_content('//div[@id="CancelTab"]/p')
        await page.wait_for_timeout(1000)
        assert validate_msg == "You Pressed Cancel", f"Expected 'You Pressed Cancel', but got '{validate_msg}'"
        
        #teardown
        await context.tracing.stop(path="logs/dialogs.zip")
        await browser.close()


#enter text in dialog box via accept

async def dialogEnterText():
   async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        await page.set_viewport_size({"width": 1800, "height": 1200})
        await page.goto("https://demo.automationtesting.in/Alerts.html")

        # Handle alert with OK and Cancel
        await page.click('a[href="#Textbox"]')
        await page.wait_for_timeout(2000)


        page.on('dialog',lambda dialog:handle_dialog(dialog))
        await page.click('button[class="btn btn-info"]')
    
        validate_msg = await page.text_content('//p[@id="demo1"]')
        await page.wait_for_timeout(2000)
        assert validate_msg == "Hello Prashant How are you today", f"Expected 'Hello Prashant How are you today', but got '{validate_msg}'"
        #You Pressed Cancel
        print(text_alert[0])
        await context.tracing.stop(path="logs/dialogs.zip")
        await browser.close()

asyncio.run(dialogEnterText())


   
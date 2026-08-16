import asyncio
from playwright.async_api import async_playwright,expect


async def main():
    async with async_playwright() as p:
        browser= await p.chromium.launch(headless=False)
        context=await browser.new_context()
        await context.tracing.start(screenshots=True,snapshots=True,sources=True)
        page=await context.new_page()

        await page.set_viewport_size({"width":1800,"height":1200})
        await page.goto("https://demoqa.com/buttons")
        
        #'button[id="eEPKU"]'
        button = page.locator("text=Click Me").nth(2)
        await button.click()
        await page.screenshot(path="screenshots/clicks.png")
        await expect(page.locator('p[id="dynamicClickMessage"]')).to_have_text("You have done a dynamic click")
        
        button2 = page.locator("text=Click Me").nth(0)
        await button2.dblclick()
        await page.screenshot(path="screenshots/dblclick.png")
        await expect(page.locator('p[id="doubleClickMessage"]')).to_have_text("You have done a double click")
       
        await context.tracing.stop(path="logs/clicks.zip")
        await browser.close()


asyncio.run(main())

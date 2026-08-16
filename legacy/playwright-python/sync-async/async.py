import asyncio
from playwright.async_api import async_playwright


async def test():
    async with async_playwright() as p:
        browser=await p.firefox.launch(headless=False)
        page=await browser.new_page()
        await page.goto("https://github-portfolio-pst99.vercel.app/")     
        print(await page.title())
    
asyncio.run(test())

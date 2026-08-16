#browser.new_context(record_video_dir='./videos')


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context(record_video_dir='./UI/videos')
    page=context.new_page()
    page.goto("https://github-portfolio-pst99.vercel.app/")
    page.screenshot(path="./UI/demo.png")
    browser.close()
    
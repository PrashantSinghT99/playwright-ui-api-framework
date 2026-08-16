from playwright.sync_api import sync_playwright

heading=[]

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    page=browser.new_page()
    
    page.goto("https://the-internet.herokuapp.com/tables")
    
    
    # heading=page.query_selector_all('//table[@id="table1"]/thead/tr/th')
    # print(len(heading))
    # for head in heading:
    #     print(head.text_content())
 
        
    table=page.query_selector('//table[@id="table1"]')
    rows=table.query_selector_all('tr')
    
    
    for row in rows:
        datas=row.query_selector_all('td')
        for data in datas:
           print(data.text_content())
    
    # datas=table.query_selector_all('td')
    
    # for data in datas:
    #     print(data.text_content())
    
    
    
    # for row in rows:
    #     datas=row.query_selector_all('td')
    #     for data in datas:
    #          print(data.text_content())
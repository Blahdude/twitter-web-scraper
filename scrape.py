from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers")
    html = page.content()
    with open("data.txt", "w") as file:
        file.write(html)
    browser.close()


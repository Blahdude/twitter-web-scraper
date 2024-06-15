from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers")

        # Query the carousel items
        carousel_items = await page.query_selector_all("li.a-carousel-card")

        with open("items.txt", 'w') as file:
            for item in carousel_items:
                # Extract the text content of the entire item
                full_text = await item.inner_text()
                title = full_text.split("\n")[1]
                rating = full_text.split("\n")[2]
                price = full_text.split("\n")[4]

                # Write the extracted title to the file
                file.write("Title: " + title + '\n' + "Rating: " + rating + '\n' + "Price: " + price + '\n\n')

        await browser.close()

# Run the main function
asyncio.run(main())

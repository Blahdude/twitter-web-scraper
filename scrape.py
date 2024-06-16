from playwright.sync_api import sync_playwright
import time

def scrape_reddit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # Navigate to the Reddit page
        page.goto("https://www.reddit.com/search/?q=bitcoin&type=link&cId=403056fd-921d-4982-8d0c-39c594f4bc17&iId=d69d4b4c-aceb-41ec-b70b-27a3b6ae4103&t=day")

        time.sleep(5)

        reddit_posts = page.query_selector_all("reddit-feed faceplate-tracker faceplate-screen-reader-content")

        with open("items.txt", 'w') as file:
            for post in reddit_posts:
                # Extract the text content of the entire item
                post_name = post.inner_text()

                file.write(post_name + '\n\n')

        browser.close()

# Run the scraping function
scrape_reddit()

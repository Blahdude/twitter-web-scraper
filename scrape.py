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
        page.goto("https://www.reddit.com/r/Bitcoin/")

        time.sleep(5)

        reddit_posts = page.query_selector_all("shreddit-feed shreddit-post")

        with open("items.txt", 'w') as file:
            i = 0
            for post in reddit_posts:
                if i > 1:
                    post_name = post.query_selector("faceplate-screen-reader-content")
                    name = post_name.inner_text() if post_name else "No title"
                    post_text = post.query_selector("p")
                    text = post_text.inner_text() if post_text else ""
                    if "Previous Actions" in text:
                        file.write(name + '\n\n')
                    else:
                        file.write(name + "\n" + "Post_text" + text + '\n\n')
                i += 1

        browser.close()

# Run the scraping function
scrape_reddit()
